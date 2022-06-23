import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", "postgres", "localhost:5432",  self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["categories"].keys()))
        self.assertTrue(len(data["questions"]))
    
    def test_404_when_get_paginated_questions_is_out_of_range(self):
        res = self.client().get("/questions?page=100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["categories"].keys()))
    
    def test_405_when_get_categories_is_a_post_request(self):
        res = self.client().post("/categories", json={'type': 'Politics'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not found")

    def test_delete_question(self):
        question = Question(question='How many atoms has Hydrogen?', answer='One', difficulty=3, category=1)
        question.insert()
        id = Question.query.filter(Question.question=='How many atoms has Hydrogen?').first().id
        res = self.client().delete("/questions/" + str(id))
        data = json.loads(res.data)
        deleted_question = Question.query.get(id)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["questions"]))
        self.assertIsNone(deleted_question)
    
    def test_422_when_trying_to_delete_nonexistent_question(self):
        res = self.client().delete("/questions/2000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Request cannot be processed")

    def test_create_question(self):
        res = self.client().post("/questions", json={'question': 'Who invented Electricity?', 'answer': 'Michael Faraday', 
        'difficulty': 2, 'category': 1})
        data = json.loads(res.data)
        created_question = Question.query.filter(Question.question=='Who invented Electricity?').all()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(created_question)
    
    def test_422_when_payload_for_create_question_is_missing(self):
        res = self.client().post("/questions", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Request cannot be processed")

    def test_search_question(self):
        res = self.client().post("/questions", json={'searchTerm': 'is'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["questions"]))
    
    def test_400_when_search_question_payload_is_invalid(self):
        res = self.client().post("/questions", json={'searchTerm': 45})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

    def test_get_question_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(data["category"], 'Science')
    
    def test_404_when_question_category_does_not_exist(self):
        res = self.client().get("/categories/1234/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    def test_get_quiz_question(self):
        res = self.client().post("/quizzes", json={'quiz_category': {'type': 'Art', 'id': 2}, 'previous_questions': [16, 17]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertNotIn(data["question"]["id"], [16, 17])
        self.assertIn(data["question"]["id"], [18, 19])
        self.assertEqual(data["question"]["category"], 2)
    
    def test_400_when_category_id_is_not_provided(self):
        res = self.client().post("/quizzes", json={'quiz_category': {}, 'previous_questions': [20, 21, 22, 26]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()