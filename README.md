# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

# API REFERENCE
## GET /categories

- Retrieves and returns all available categories in a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request arguments (parameters): None,
- Response body :{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}

## GET /questions

- Fetches and returns a set of questions(paginated ,10 questions per page ), a total number of questions, all categories ,the sucess value and current category string.

- Request arguments (paramter): Page number

- Response body :{
    'questions': [
        {
            'id': 2,
            'question': 'Answer this question',
            'answer': 'Here  is the answer',
            'difficulty': 3,
            'category': 1
        },
    ],
    'totalQuestions': 20,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'Science',
    'success':True

}

## GET /categories/int:category_id/questions

- Fetches questions for a specified category (specified by the id given as the request argument)

- Request arguments(parameter): category id

- Returns an object of all questions in a given category, total questions, current category and success value
- Response body :{
    'questions': [
        {
            'id': 2,
            'question': 'Answer this question',
            'answer': 'Here  is the answer',
            'difficulty': 3,
            'category': 1
        },
    ],
    'totalQuestions': 20,
    'currentCategory': 'Science',
    'success':True
}

## DELETE /questions/int:question_id

- Deletes a specified question using the  question id passed as the request argument

- Request arguments (parameters): question id (integer)

- Returns the ID of the deleted question and the success value
- Response body :{
                "success": True,
                "deleted": question_id,
                "totalQuestions": len(available_questions),
                "questions":current_questions
            }
## POST /quizzes

- Gets (next )question needed to play the quiz. 
- Request arguments: The quiz category and question IDs of previous questions
{
    'previous_questions': [1, 14]
    quiz_category': 'Arts'
 }

- Returns a single question object  fetched from the selected category
- Response body :questions': 
        {
            'id': 2,
            'question': 'Answer this question',
            'answer': 'Here  is the answer',
            'difficulty': 3,
            'category': 1
        }
        
## POST /questions

- Creates a new question that is added to the trivia database

- Request arguments: {
    'question':  'a new question string',
    'answer':  'a new answer string',
    'difficulty': 1,
    'category': 2,
}

- Returns a success value(True or False) and the id of the new question

## POST /questions/search

- Searches for a specific question by search term (given as request parameter/argument)
- Request argument: a search term
{
    'searchTerm': 'this is the question I want to see'
}

- Returns any array of questions, a number of totalQuestions that met the search term and the current category string.

## Errors

### Error 404

- Returns a json object with keys: success, error and message.

- {"success": false, "error": 404, "message": "resource not found"}
- 
### Error 400

- Returns a json object with keys: success, error and message.

- {"success": false, "error": 400, "message": "bad request"}
### Error 405

- Returns a json object with keys: success, error and message.

- {"success": False, "error": 405, "message": "method not allowed"})

### Error 500

- Returns a json object with keys: success, error and message.

- {"success": false, "error": 500, "message": "internal server error"}
### Error 422

- Returns a json object with keys: success, error and message.

- {"success": false, "error": 422, "message": "unprocessable"}
Testing

## To run the tests on the flask app, run in the backend folder:

```dropdb trivia_test , createdb trivia_test,  psql trivia_test < trivia.psql,  python3 test_flaskr.py```(respectively)

