from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests

app=Flask(__name__)
app.secret_key="secret key"
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/CRUD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
class library(db.Model):
    isbn=db.Column(db.String(100),primary_key = True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))
    id = db.Column(db.String(100))
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))




    def __init__(self,isbn,title, author,Id=' ',name=' ',email=' '):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.id = Id
        self.name=name
        self.email=email




@app.route('/')
def Index():
    all_data=library.query.all()
    return render_template("index.html", employees = all_data)
@app.route('/issue', methods=['GET', 'POST'])
def issue():
    if request.method=='POST':
        my_data=library.query.get(request.form.get('isbn'))
        my_data.isbn = request.form['isbn']
        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.name=request.form['Name']
        my_data.email=request.form['Email']
        my_data.id=request.form['Id']
        db.session.add(my_data)
        db.session.commit()
        flash("issue successful")
        return redirect(url_for('Index'))


@app.route('/insert', methods = ['post'])
def insert():
    if request.method=='POST':
        isbn = request.form['isbn']
        title= request.form['title']
        author = request.form['author']
        id = request.form['Id']
        name = request.form['Name']
        email = request.form['Email']
        mydata=library(isbn,title, author, id,name,email)
        db.session.add(mydata)
        db.session.commit()
        flash("Book inserted successfully")

        return redirect(url_for('Index'))
@app.route('/returnbook', methods = ['GET', 'POST'])
def returnbook():
    if request.method == 'POST':
        my_data = library.query.get(request.form.get('isbn'))
        my_data.isbn = request.form['isbn']
        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.name = ' '
        my_data.email = ' '
        my_data.id = ' '
        db.session.add(my_data)
        db.session.commit()
        flash("book returned sucessfully...book is no longer tagges to your name")
        return redirect(url_for('Index'))

@app.route('/getbooks', methods = ['GET', 'POST'])
def getbooks():
    url = 'https://frappe.io/api/method/frappe-library?page=2&title=and'
    response = requests.get(url)
    book_dictionary = response.json()
    for key in book_dictionary:

        for element in book_dictionary[key]:

            for key1 in element:
                if key1 == 'isbn':
                    isbn = element[key1]
                if key1=='title':

                    title = element[key1]
                if key1=='authors':

                    author = element[key1]
            mydata = library(isbn, title, author)
            db.session.add(mydata)
            db.session.commit()
    return redirect(url_for('Index'))


