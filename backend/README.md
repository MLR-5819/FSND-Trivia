# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints
- GET '/categories'
- GET '/questions'
- DELETE '/questions/<int:question_id>'
- POST '/questions'
- POST '/questions/search'
- GET '/categories/<int:cat_id>/questions'
- POST '/quiz'

### GET '/categories'
- Fetches: A dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object of id: category_string  
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```
### GET '/questions'
- Fetches: A dictionary of categories like above, an object containing dictionaries of all questions in the database, and then a success message as well as total number of questions.
- Request Arguments: None
- Returns: An object of categories{cat_id: cat_string}; questions {id, category, question, answer, difficulty}; success message, and total number of questions
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {...cut out other questions...}
  ],
  "success": true,
  "total_questions": 18
}
```  
### DELETE '/questions/<int:question_id>'
- Fetches: a single particular question to delete from the database
- Request Arguments: Question_id
- Returns: An object confirming id of deleted questions and displays all other questions left like above.
```
{
  "deleted": 6,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {...cut out other questions...}
  ],
  "success": true,
  "total_questions": 17
}
```

### POST '/questions'
- Fetches: input from the user to add a new question to the database
- Request Arguments: user must submit a 'Question', 'Answer', 'Difficulty', and 'Category'
- Returns: an object confirming created question id and displays all other questions like above. 
```
{
  "created": 55,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {...cut out other questions...}
  ],
  "success": true,
  "total_questions": 18
}
```

### POST '/questions/search'
- Fetches: any question that contains the search term the user enters
- Request Arguments: searchTerm -example used 'grammy'
- Returns: An object containing any question matching the searchTerm, success message, and total number of questions matching the searchTerm.
```
{
  "questions": [
    {
      "answer": "Beyonce, 63 Grammy nominations",
      "category": 5,
      "difficulty": 3,
      "id": 55,
      "question": "Which female singer has the most Grammy nominations?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

### GET '/categories/<int:cat_id>/questions'
- Fetches: All questions from the category that the user clicks on
- Request Arguments: cat_id
- Returns: An object containing selected category, all questions in that category, success message, and total number of questions in that category.
```
{
  "current_category": "History",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### POST '/quiz'
- Fetches: A single question from the selected category
- Request Arguments: Category selection, any previous questions already asked
- Returns: An object containing the random question from the selected category and a success message.
```
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```