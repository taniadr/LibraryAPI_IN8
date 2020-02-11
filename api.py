#!/usr/bin/python
# -*- encoding:utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

#this will be for proper control of books in/out
class Controle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookId = db.Column(db.Integer, nullable=False)
    userName = db.Column(db.String(200), nullable=False)
    dateBorrow = db.Column(db.DateTime, default=datetime.utcnow)
    dateReturn = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Controle %r>' % self.id


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
    book = Library.query.get_or_404(id)

    if request.method == 'POST':
        book.title = request.form['content_title']
        book.author = request.form['content_author']
        book.year_published = request.form['content_year']
        book.status = request.form['content_status']

        try: 
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the book'
    
    else:
        return render_template('update.html', book=book)

if __name__ == "__main__":
    app.run(debug=True)
