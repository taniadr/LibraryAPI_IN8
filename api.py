from flask import Flask, request, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(60), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.id

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
            return 'There was an issue adding the book'

    else:
        books = Library.query.order_by(Library.author).all()
        return render_template('index.html', books=books)


@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete = Library.query.get_or_404(id)

    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the book'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    book_to_update = Library.query.get_or_404(id)

    if request.method == 'POST':
        book_to_update.title = request.form['content_title']
        book_to_update.author = request.form['content_author']
        book_to_update.year_published = request.form['content_year']
        book_to_update.status = request.form['content_status']
        
        try: 
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the book'
    
    else:
        return render_template('update.html', book=book_to_update)

if __name__ == "__main__":
    app.run(debug=True)
