import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app,QUESTIONS_PER_PAGE
from models import setup_db, Question, Category
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv('USER')
PASSWORD = os.getenv('PASS')
HOST =  os.getenv('DB_HOST')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.new_quiz = {
            "quiz_category": {"id": 2, "type": "Art"},
            "previous_questions": [1,2,3]
        }
        self.search ={
            'searchTerm': 'movie'}


        self.new_question={
                'question':  'Heres a new question string',
                'answer':  'Heres a new answer string',
                'difficulty': 2,
                'category': 1,
            }

        self.new_question_422 = {
            "answer": "Heres a new answer string",
            "category": 2
        }


        self.quiz_422 = {
            "current_category": {},
            "previous_questions": {}
        }
        
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(USERNAME,PASSWORD,HOST, self.database_name)
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
    def test_retrieve_categories(self):
        res=self.client().get("/categories")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertEqual(len(data["categories"]),data["total_categories"])

        self.assertTrue(data["categories"])
        self.assertTrue(data["total_categories"])

    
    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
    
    def test_404_request_beyond_valid_page(self):
        res = self.client().get('/questions?page=97')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        questions = Question.query.all()
        question = questions[0].format()
        res = self.client().delete(f"/questions/{question['id']}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], question['id'])
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])

    def test_404_not_found_delete_question(self):
        res = self.client().delete("/questions/65")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['created'])

    def test_422_unprocessable_new_question(self):
        res = self.client().post("/questions", json=self.new_question_422)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], "unprocessable")
        self.assertTrue(data['error'])
    
    def test_search_questions(self):
            res = self.client().post("/questions", json= self.search)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertIsNotNone(data['questions'])
            self.assertIsNotNone(data['totalQuestions'])
    
    def test_retrieve_category_questions(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['currentCategory'], 'Science')
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["questions"])
        self.assertIsNotNone(data['totalQuestions'])

    def test_404_not_found_retrieve_category_questions(self):
        res = self.client().get("/categories/1000/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_retrieve_quiz(self):
        res = self.client().post("/quizzes", json=self.new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    def test_422_unprocessable_retrieving_quiz(self):
        res = self.client().post("/quizzes", json=self.quiz_422)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], "unprocessable")
        self.assertTrue(data['error'])





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()