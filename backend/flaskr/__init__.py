import os
from xmlrpc.client import SERVER_ERROR, Server
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10
def paginate_questions(request,selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app,resources={r"/api/*":{"origins":"*"}})

    """
    # CORS HEADER
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,true")
        response.headers.add("Access-Contol-Allow-Methods","GET,PUT,POST,DELETE,OPTIONS")
        return response


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def retrieve_categories():
        try:
            available_categories=Category.query.all()
            formatted_categories={category.id: category.type for category in available_categories}
            return jsonify({
                "success":True,
                'categories':formatted_categories,
                "total_categories":len(available_categories)

        })
        except:
           abort(404)


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
    @app.route('/questions',methods=['GET'])
    def retrieve_questions():
        available_questions=Question.query.order_by(Question.id).all()
        categories=Category.query.order_by(Category.id).all()
        formatted_categories={category.id: category.type for category in categories}
        current_questions=paginate_questions(request,available_questions)
        if len(current_questions) == 0:
            abort(404)
        return jsonify(
            {
                "success":True,
                "questions": current_questions,
                "total_questions": len(available_questions),
                "categories":formatted_categories,
                "current_category":formatted_categories[current_questions[-1]['category']
                ]
            }
        )


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>',methods=['GET','DELETE'])
    def delete_question(question_id):
        try:
            question_to_delete =Question.query.get(question_id)
            if question_to_delete is None:
                abort(404)
            question_to_delete.delete()
            available_questions= Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, available_questions)

            return jsonify({
                "success": True,
                "deleted": question_id,
                "totalQuestions": len(available_questions),
                "questions":current_questions
            })
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

        """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions',methods=['GET','POST'])
    def create_or_search_questions():
        body=request.get_json()
        search_term = body.get('searchTerm', None)

        new_question=body.get("question",None)
        new_answer=body.get("answer",None)
        category=body.get("category",1)
        difficulty=body.get("difficulty",1)
        if (new_question == None or new_answer == None) and search_term is None:
            abort(422)
        try:
            if search_term:
                available_questions = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search_term))).all()
                current_questions = paginate_questions(request, available_questions)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'totalQuestions': len(current_questions),
                    "currentCategory":Category.query.get(current_questions[-1]['category']).type
                })
            else:
                question = Question(question=new_question, answer=new_answer, category=category, difficulty=difficulty)
                question.insert()

                questions = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'created': question.id,
                }), 201
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_category_questions(category_id):
        try:
            category_questions=Question.query.filter(Question.category == category_id).all()
            formatted_questions=[question.format() for question in category_questions]
            return jsonify({
                'success':True,
                'questions':formatted_questions,
                'totalQuestions':len(category_questions),
                'currentCategory':Category.query.get(category_id).type
            })
        except:
            abort(404)

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
    @app.route("/quizzes",methods=['POST'])
    def retrieve_quizzes():
        body=request.get_json()
        current_category=body.get("quiz_category")
        previous_questions=body.get("previous_questions")
        random_question=None
        try:
            if current_category is None or current_category['id'] == 0:
                category_questions =[question.format() for question in Question.query.all()]
            else:
                category_questions=[question.format() for question in Question.query.filter(Question.category == current_category['id']).all()] 
            random.shuffle(category_questions)
            questions=[]
            for question in category_questions:
                if question['id'] not in previous_questions:
                    questions.append(question)
                
            if (len(questions) > 0):
                random_question = random.choice(questions)
                    
            return jsonify({
                'success': True,
                'question': random_question,
                'previous_questions': previous_questions
            })   
        except:
            abort(422)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return ( jsonify({
            "success":False,
            "error":404,
            "message":"resource not found"        
            }),404,)

    
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )
    
    @app.errorhandler(500)
    def bad_request(error):
        return (jsonify({"success": False, "error": 500, "message": "internal server error"}), 500)

    return app

