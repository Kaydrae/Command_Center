from flask_login import LoginManager
from database import LoginResult, database_interface


class User:
    def __init__(self, user_id=None):
        # required fields for flask-login
        self.id = user_id
        self.email = None
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = False

    # attempt to login the user
    def login(self, email, password):
        # check if the email exists in the DB and if the password is correct
        login_result = database_interface.login(email, password)

        if login_result == LoginResult.SUCCESS:
            # get the users id and set it
            self.id = database_interface.get_user_id(email)

            # set the users email
            self.email = email

            # set the user as authenticated
            self.is_authenticated = True

            # return the login result
            return login_result

        # set the user as unauthenticated
        self.is_authenticated = False

        # return the result of the login attempt
        return login_result

    # return the ID
    def get_id(self):
        return self.id

    # reload the User with data given its ID
    @staticmethod
    def get(user_id):
        # callback for returning a new user given the user_id
        new_user = User(user_id)

        # get the users email
        new_user.email = database_interface.get_user_email(user_id)

        # return the new user
        return new_user


login_manager = LoginManager()


def init_login(app):
    login_manager.init_app(app)


# used to reload the user session given their ID
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
