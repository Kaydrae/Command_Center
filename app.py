from flask import Flask, render_template, redirect, request
from flask_socketio import SocketIO, emit, join_room
from flask_login import login_user, logout_user
from login import User, login_manager
from forms import LoginForm
from database import database_interface
from iot import device_manager
from iotmanager import Manager
import logging

iot_app_logger = logging.basicConfig()

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = ''

# iot manager instance
iot_manager = Manager(["rgb_light"], host="0.0.0.0")


@app.route('/')
def home():
    data = iot_manager.get_client_data()

    return render_template("control.html", device_data=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # form submission validator
    form = LoginForm()

    print(form.validate())

    # check if the submitted form is valid
    if form.validate() and request.method == "POST":
        # verify the user login
        user = User()

        print("logging in with creds: Email: " + str(form.email) + " | Password: " + str(form.password))

        user.login(form.email, form.password)

        print("logged in successful")

        # login the user to the server
        login_user(user=user)

        # redirect back to the home page view
        return redirect("/")

    # else load the login page
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    # logout the user
    logout_user()

    # redirect the user to the home page
    return redirect("/")


if __name__ == '__main__':
    app.run()
