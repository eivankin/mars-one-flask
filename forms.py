from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    IntegerField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    login = StringField('Login / E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat password',
                                    validators=[DataRequired(), EqualTo('password')])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Login / E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class JobForm(FlaskForm):
    job = StringField('Job title', validators=[DataRequired()])
    team_leader = IntegerField('Team Leader ID', validators=[DataRequired()])
    work_size = IntegerField('Work size (hours)', validators=[DataRequired()])
    collaborators = StringField('Collaborators IDs (comma-separated)',
                                validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')


class DepartmentForm(FlaskForm):
    chief = IntegerField('Chief ID', validators=[DataRequired()])
    title = StringField('Title of Department', validators=[DataRequired()])
    members = StringField('Members IDs (comma-separated)',
                          validators=[DataRequired()])
    email = EmailField('Department E-mail', validators=[DataRequired()])
    submit = SubmitField('Submit')
