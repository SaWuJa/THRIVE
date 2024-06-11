from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from thrive.models import User


class RegisterForm(FlaskForm):
    # Custom validation to ensure username uniqueness
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')

    # Custom validation to ensure email address uniqueness
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('This email address is already in use. Please use a different email.')

    username = StringField('Username:', validators=[
        DataRequired(message="A username is required."),
        Length(min=2, max=30, message="Username must be between 2 and 30 characters.")
    ])

    email_address = StringField('Email Address:', validators=[
        DataRequired(message="An email address is required."),
        Email(message="Please enter a valid email address.")
    ])

    password1 = PasswordField('Password:', validators=[
        DataRequired(message="Please enter a password."),
        Length(min=6, message="Password must be at least 6 characters.")
    ])

    password2 = PasswordField('Confirm Password:', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password1', message="Passwords do not match.")
    ])

    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(message="Please enter your username.")])
    password = PasswordField('Password:', validators=[DataRequired(message="Please enter your password.")])
    submit = SubmitField('Log In')

class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Project')
