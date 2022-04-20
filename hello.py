# from crypt import methods
from distutils.log import error
import email
from enum import unique
import imp
from unicodedata import name
from wsgiref.validate import validator
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# secret key
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

#initialize the db
db = SQLAlchemy(app)

# create a model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create a str
    def __repr__(self):
        return '<Name %r>' % self.name

#create a Form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


#create a Form class
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("USer added successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


@app.route('/')
def index():
    flash("Welcome to my blog!")
    my_name="Palash"
    my_stuff="Weather is quite <i>pleseant</i> today"
    fav_player=["L.Sen", "LinD", "LCW"]
    return render_template('index.html', my_name=my_name, stud=my_stuff, fav_player=fav_player)




@app.route('/user/<name>')
def user(name):
    # return "<h1>Hello {}</h1>".format(name)
    return render_template('user.html', user_name=name)

#internal server error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html') 


#Create a name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    #Vaildate form 
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submitted successfully")

    return render_template("name.html", 
            name = name,
            form = form)
