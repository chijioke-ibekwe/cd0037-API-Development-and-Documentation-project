# API Documentation

## Trivia App

This application contains the following endpoints:

1. GET '/categories'

This endpoint fetches the various categories of questions available on the app. The questions are categorized according to subject matter.

Request Arguments: None

Returns: An object containing the id and name of each category in key:value pairs.

{
    'categories': { 
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" 
    }
}

2. GET '/questions?page=${integer}'

This endpoint fetches a list of objects containing the details of each question available on the app in batches of 10 (10 questions per page), as well as other related details regarding the question categories and number of questions available.

Request Arguments: 'page' query parameter (integer)

Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'Who invented Electricity?',
            'answer': 'Michael Faraday',
            'difficulty': 3,
            'category': 1
        },
    ],
    'totalQuestions': 100,
    'categories': { 
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" 
    },
    'currentCategory': 'Science'
}

3. DELETE '/questions/${question_id}'

This endpoint deletes a question from the app using the id, and returns a list of objects containing the details of the remaining questions.

Request Arguments: question_id (integer)

Returns: An object with 10 paginated questions and the total number of questions remaining.

{
    'questions': [
        {
            'id': 1,
            'question': 'In what continent is India located?',
            'answer': 'Asia',
            'difficulty': 2,
            'category': 3
        },
    ],
    'totalQuestions': 15
}

4. POST '/questions'

This endpoint handles two different requests: A request to search for a question using a substring of the question and a request to create a new question. Both of these requests have different bodies and expected responses.

Request Bodies:
For the request to search for a question, the body contains only a searchTerm property as shown below:

{
    'searchTerm':  '1990'
}

While for the request to create a new question, the body takes four properties: question, answer, difficulty level and category:

{
    'question':  'What is the atomic number of Lithium?',
    'answer':  'Three',
    'difficulty': 2,
    'category': 1,
}

Returns: 
The request to search for a question using a substring returns an object that contains a paginated list of questions (10 questions per page) that contain the search term, the total number of questions that contain the search term, and the current category.

{
    'questions': [
        {
            'id': 1,
            'question': 'Who invented Electricity?',
            'answer': 'Michael Faraday',
            'difficulty': 3,
            'category': 1
        },
    ],
    'totalQuestions': 1,
    'currentCategory': 'Science'
}

The request to create a new question returns a paginated list of questions that are now availabele on the app, along with the total number of questions.

{
    'questions': [
        {
            'id': 1,
            'question': 'In what continent is India located?',
            'answer': 'Asia',
            'difficulty': 2,
            'category': 3
        },
    ],
    'totalQuestions': 15
}

5. GET '/categories/${category_id}/questions'

This endpoint fetches a list of objects containing the details of all the questions on the app that fall in the specified category, in batches of 10 (10 questions per page).

Request Arguments: category_id (integer)

Returns: An object with questions for the specified category, total questions, and current category string

{
    'questions': [
        {
            'id': 1,
            'question': 'In what continent is India located?',
            'answer': 'Asia',
            'difficulty': 2,
            'category': 3
        },
    ],
    'totalQuestions': 15,
    'currentCategory': 'Geography'
}

6. POST '/quizzes'

This endpoint simulates a game and returns a random question that belong to the category specified and that has not been previously returned.

Request Body:
{
    'previous_questions': [12, 24, 36]
    'quiz_category': {type: 'Entertainment', 'id': 5}
}

Returns: A single question object
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}
