from wtforms import Form, StringField, ValidationError, validators
import re
import hashlib


class LoginForm(Form):
    def __init__(self):
        super().__init__()

        self.email = StringField(u'email', validators=[validators.email, validators.input_required])
        self.password = StringField(u'password', validators=[validators.input_required])

    @staticmethod
    def validate_email(form, field):
        if field.data.endswith("@uat.edu"):
            return
        else:
            raise ValidationError("email does not end in valid suffix")

    @staticmethod
    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError("password is too short")
        if re.search("[a-z]", field.data):
            raise ValidationError("no lowercase char")
        if re.search("[A-Z]", field.data):
            raise ValidationError("no uppercase char")
        if re.search("[0-9]", field.data):
            raise ValidationError("no number")
        else:
            return

