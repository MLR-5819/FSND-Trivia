import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

#Environment setup: set FLASK_APP=flaskr; set FLASK_ENV=development

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  #@DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  cors = CORS(app, resources={r"/*": {"orgins": "*"}})
  
  #DONE: Use the after_request decorator to set Access-Control-Allow
  #CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
  
  #DONE: Create an endpoint to handle GET requests for all available categories.
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    curr_categories = {}

    for category in categories:
      curr_categories[category.id] = category.type

    if len(curr_categories) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "categories": curr_categories
    })

  #@DONE: 
  #Create an endpoint to handle GET requests for questions, 
  #including pagination (every 10 questions). 
  #This endpoint should return a list of questions, 
  #number of total questions, current category, categories. 
  #TEST: At this point, when you start the application
  #you should see questions and categories generated,
  #ten questions per page and pagination at the bottom of the screen for three pages.
  #Clicking on the page numbers should update the questions. 
  @app.route('/questions', methods=['GET'])
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    curr_questions = paginate_questions(request, selection)
    categories = Category.query.order_by(Category.id).all()
    curr_categories = {}

    for category in categories:
      curr_categories[category.id] = category.type

    if len(curr_categories) == 0:
      abort(404)

    if len(curr_questions) == 0:
      abort(404)
    
    return jsonify({
      "success": True,
      "categories": curr_categories,
      "questions": curr_questions,
      "total_questions": len(Question.query.all())
    })

  #@DONE: 
  #Create an endpoint to DELETE question using a question ID. 
  #TEST: When you click the trash icon next to a question, the question will be removed.
  #This removal will persist in the database and when you refresh the page. 
  
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      curr_questions = paginate_questions(request, selection)

      return jsonify({
        "success": True,
        "deleted": question_id,
        "questions": curr_questions,
        "total_questions": len(Question.query.all())
      })
    
    except:
      abort(422)

  #@DONE: 
  #Create an endpoint to POST a new question, 
  #which will require the question and answer text, 
  #category, and difficulty score.
  #TEST: When you submit a question on the "Add" tab, 
  #the form will clear and the question will appear at the end of the last page
  #of the questions list in the "List" tab.  
  
  @app.route('/questions', methods=['POST'])
  def create_question():
    form = request.get_json()

    new_question = form.get('question', None) 
    new_answer = form.get('answer', None)
    new_diff = form.get('difficulty', None)
    new_category = form.get('category', None)

    try:
      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_diff)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      curr_questions = paginate_questions(request, selection)

      return jsonify({
        "success": True,
        "created": question.id,
        "questions": curr_questions,
        "total_questions": len(Question.query.all())
      })

    except:
      abort(422)

  #@DONE: 
  #Create a POST endpoint to get questions based on a search term. 
  #It should return any questions for whom the search term 
  #is a substring of the question. 
  #TEST: Search by any phrase. The questions list will update to include 
  #only question that include that string within their question. 
  #Try using the word "title" to start. 
  
  @app.route('/questions/search', methods=['POST'])
  def search():
    try:
      search_form = request.get_json()
      search_term = search_form.get('searchTerm', None)
      
      selection = Question.query.order_by(Question.id).filter(Question.question.ilike(f'%{search_term}%'))
      curr_questions = paginate_questions(request, selection)

      return jsonify({
        "success": True,
        "questions": curr_questions,
        "total_questions": len(selection.all())
      })

    except:
      abort(422)
  
  #@DONE: 
  #Create a GET endpoint to get questions based on category. 
  #TEST: In the "List" tab / main screen, clicking on one of the 
  #categories in the left column will cause only questions of that 
  #category to be shown. 
  
  @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
  def category_list(cat_id):
    try:
      cat_select = Category.query.filter(Category.id == cat_id).one_or_none()
      selection = Question.query.filter(Question.category == cat_id).all()
      curr_questions = paginate_questions(request, selection)
      
      return jsonify({
        "success": True,
        "questions": curr_questions,
        "total_questions": len(selection),
        "current_category": cat_select.type
      })

    except:
      abort(422)
  
  #@TODO: 
  #Create a POST endpoint to get questions to play the quiz. 
  #This endpoint should take category and previous question parameters 
  #and return a random questions within the given category, 
  #if provided, and that is not one of the previous questions. 
  #TEST: In the "Play" tab, after a user selects "All" or a category,
  #one question at a time is displayed, the user is allowed to answer
  #and shown whether they were correct or not. 
  
  #@app.route('/quiz', methods=['POST'])
  #def play_quiz():



  #@DONE:Create error handlers for all expected errors 
  #including 404 and 422. 
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request"
    }), 400
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource Not Found"
    }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable"
    }), 422

    #TODO check if anymore errorhandlers needed
  
  
  return app