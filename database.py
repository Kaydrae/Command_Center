from enum import Enum
from sqlalchemy import create_engine, exc
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from passlib.hash import pbkdf2_sha512
from password_strength import PasswordPolicy
from uuid import uuid4
import logging


# login result Enum
class LoginResult(Enum):
    SUCCESS = "SUCCESS"
    UNVERIFIED_ACCOUNT = "UNVERIFIED_ACCOUNT"
    INCORRECT_PASSWORD = "INCORRECT_PASSWORD"
    FAIL = "FAIL"


# new account result Enum
class NewAccountResult(Enum):
    SUCCESS = "SUCCESS"
    EXISTING_ACCOUNT = "EXISTING_ACCOUNT"
    WEAK_PASSWORD = "WEAK_PASSWORD"
    FAIL = "FAIL"


# password strength requirements
password_policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=2,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)


class DatabaseManager:
    def __init__(self):
        self.__logger = logging.Logger("DB Manager")
        engine_started = False

        while not engine_started:
            try:
                # logging
                self.__logger.info("Creating SQLAlchemy Engine")

                # make a db connection object
                self.engine = create_engine('mysql://engineeringmysql:EngineeringMySQL2020$'
                                            '@10.10.1.126:3306/iot_app')

                # logging
                self.__logger.info("Connecting to DB")

                # connect to the db
                self.engine.connect()

                # logging
                self.__logger.info("DB Connected Successfully")

                # mark that the engine has been started to end the while loop
                engine_started = True
            except exc.SQLAlchemyError as e:
                self.__logger.error("DB Failed to Connect")
        return

    # attempt to login a user given their email and password
    def login(self, email, password):
        # get a hash of the password
        password_hash = pbkdf2_sha512.hash(password)

        # check if a user exists with the given username and password
        result = self.engine.execute("SELECT * FROM users WHERE email=%s", email).first()

        # if a user exists with the given email
        if result is not None:
            # if the stored password hash does not match the password
            if not pbkdf2_sha512.verify(password, result["password"]):
                return LoginResult.INCORRECT_PASSWORD

            # check if they are verified
            if result[0]["verified"]:
                # return the login as a success
                return LoginResult.SUCCESS

            # return that the account is unverified
            return LoginResult.UNVERIFIED_ACCOUNT

        # account login was a failure
        return LoginResult.FAIL

    # attempt to create a new account
    def new_account(self, email, password):
        # check if the email the user provides is already in use
        result = self.engine.execute("SELECT * FROM users WHERE email=%s", email).first()

        # if the username is in use
        if result is not None:
            # return that an account already exists
            return NewAccountResult.EXISTING_ACCOUNT

        if len(password_policy.test(password)) != 0:
            return NewAccountResult.WEAK_PASSWORD

        # generate a password hash
        password_hash = pbkdf2_sha512.hash(password)

        # generate a id for the user
        user_id = self.get_unique_id()

        try:
            # create the new user
            self.engine.execute("INSERT INTO users VALUES (%s, %s, %s, %s)",
                                (user_id, email, password_hash, "false"))
        except exc.SQLAlchemyError:
            # if an exception occurs return a FAIL
            return NewAccountResult.FAIL

        # if everything passes return SUCCESS
        return NewAccountResult.SUCCESS

    # gets the users id based upon their email
    def get_user_id(self, email):
        # check if the email the user provides is already in use
        result = self.engine.execute("SELECT id FROM users WHERE email=%s", email).first()

        # return None if no entry's were found
        if result is None:
            return None

        # return the id if it was found
        return result["id"]

    # gets the users id based upon their email
    def get_user_email(self, user_id):
        # check if the email the user provides is already in use
        result = self.engine.execute("SELECT email FROM users WHERE id=%s", user_id).first()

        # return None if no entry's were found
        if result is None:
            return None

        # return the id if it was found
        return result["email"]

    # generates a unique uuid for use in user ids (checks DB)
    def get_unique_id(self):
        # loop until unique id is generated
        while True:
            # generate a id
            user_id = str(uuid4())

            # check the database
            result = self.engine.execute("SELECT * FROM users WHERE id=%s", user_id).first()

            # if it exists
            if result is not None:
                # generate new id
                continue

            # return the unique id
            return user_id


# create an instance of the database manager for global use
database_interface = DatabaseManager()
