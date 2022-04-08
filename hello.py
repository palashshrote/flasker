from distutils.log import error
from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def index():
    my_name="Palash"
    my_stuff="Weather is quite <i>pleseant</i> today"
    fav_player=["L.Sen", "LinD", "LCW"]
    return render_template('index.html', my_name=my_name, stud=my_stuff, fav_player=fav_player)




@app.route('/user/<name>')
def user(name):
    # return "<h1>Hello {}</h1>".format(name)
    return render_template('user.html', user_name=name)


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html')

