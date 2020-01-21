import flask
from flask import request, jsonify, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True
    
#Mock Objects
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'year_published': '1992',
     'status': 'available'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'published': '1973',
     'status': 'available'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel Delany',
     'published': '1975',
     'status': 'available'},
     {'id': 3,
     'title': 'Zen Para Distraidos',
     'author': 'Monja Coen',
     'published': '2017',
     'status': 'available'},
     {'id': 4,
     'title': 'A Monja e o Professor',
     'author': 'Monja Coen',
     'published': '2018',
     'status': 'available'},
     {'id': 5,
     'title': 'Aprenda a Viver o Agora',
     'author': 'Monja Coen',
     'published': '2019',
     'status': 'available'},
     {'id': 6,
     'title': 'A Sabedoria da Transformação',
     'author': 'Monja Coen',
     'published': '2014',
     'status': 'available'}

]

@app.route('/')
@app.route('/index')
def index():

    displays = []

    for book in books:
        temp = book['author']
        if temp in displays:
            temp = 'nada' #in order to avoid repetition of authors
        else:   
            displays.append(temp)

    return render_template('index.html', title='The Library API', authors=displays)

#This route returns all books in the database
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

#This method requires a number input (book id)
@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


# this route requires a string input (author)
# test the function below using:
# http://localhost:5000/api/v1/resources/authors?author=Monja Coen
@app.route('/api/v1/resources/authors', methods=['GET'])
def api_authors():
    if 'author' in request.args:
        author = str(request.args['author'])
    else:
        return "Error: No author name provided. Please specify one."
     
    results = []

    for book in books:
        if book['author'] == author:
            results.append(book)
    
    return jsonify(results)

#@app.route('/api/v1/resources/available', methods=['GET'])
#def api_available():

app.run()