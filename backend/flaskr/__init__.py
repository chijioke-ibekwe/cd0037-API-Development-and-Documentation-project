import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in selection]
    current_questions = formatted_questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        categories = Category.query.all()
        data={}

        for category in categories:
            data[category.id] = category.type

        return jsonify({
            "categories": data
            })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_all_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.all()
        categories_data={}

        if len(current_questions) == 0:
            abort(404)
        
        for category in categories:
            categories_data[category.id] = category.type

        return jsonify({
            'questions': current_questions,
            'totalQuestions': len(questions),
            'categories': categories_data,
            'currentCategory': categories_data[1]
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get_or_404(question_id)
            question.delete()
            questions = Question.query.all()
            current_questions = paginate_questions(request, questions)
            
            return jsonify({
                'questions': current_questions,
                'totalQuestions': len(questions)
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.

    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        payload = request.get_json()
        if payload.get('searchTerm') is not None:
            try:
                questions = Question.query.filter(Question.question.ilike('%' + payload.get('searchTerm') + '%')).order_by(Question.id).all()
                current_questions = paginate_questions(request, questions)
                current_category = Category.query.get(int(current_questions[0]["category"]))

                return jsonify({
                    'questions': current_questions,
                    'totalQuestions': len(questions),
                    'currentCategory': current_category.type
                })
            except:
                abort(400)
        else:
            try:
                question = Question(question=payload.get('question'), answer=payload.get('answer'), difficulty=int(payload.get('difficulty')), 
                category=int(payload.get('category')))
                question.insert()
                questions = Question.query.all()
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'questions': current_questions,
                    'totalQuestions': len(questions),
                })
            except:
                abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category = Category.query.get_or_404(category_id)
        questions = Question.query.filter(Question.category==category_id).order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        return jsonify({
            'questions': current_questions,
            'totalQuestions': len(questions),
            'category': category.type
        })
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        body = request.get_json()
        category_id = body.get('quiz_category').get('id')
        previous_questions = body.get('previous_questions')

        if category_id is None:
            abort(400)

        if int(category_id) == 0:
            questions = Question.query.filter(~Question.id.in_(previous_questions)).order_by(Question.id).all()
        else:
            questions = Question.query.filter(Question.category==int(category_id), ~Question.id.in_(previous_questions)).order_by(Question.id).all()
        
        if len(questions) == 0:
            return jsonify({
            'question': None
        })

        length = len(questions)
        random_question = questions[random.randrange(length)].format()

        return jsonify({
            'question': random_question
        })


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Request cannot be processed'
        }), 422

    @app.errorhandler(405)
    def method_not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not found'
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500
    return app

