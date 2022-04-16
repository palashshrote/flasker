# from crypt import methods
from distutils.log import error
import imp
from unicodedata import name
from wsgiref.validate import validator
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

#create a Form class
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


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
