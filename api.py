import flask
from flask import Flask, request, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(60), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Book %r>' % self.title

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        c_title = request.form['content_title']
        c_author = request.form['content_author']
        c_year = request.form['content_year']
        c_status = request.form['content_status']
        new_book = Library(title=c_title, author=c_author, year_published=c_year, status=c_status)

        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your book'


    else:
        books = Library.query.order_by(Library.author).all()
        return render_template('index.html', books=books)


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
if __name__ == "__main__":
    app.run(debug=True)