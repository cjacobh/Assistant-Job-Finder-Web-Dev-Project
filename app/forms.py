from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField, IntegerField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Length, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

from app.models import User

class UserForm(FlaskForm):
    tof = SelectField('Role', choices = [(1, 'TA'), (2, 'Faculty')])
    username = StringField('Username', validators=[DataRequired()])
    fullname = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    phonenum = StringField('Phone Number', validators=[DataRequired()])
    wsuid = StringField('WSU ID', validators=[DataRequired()])
    major = SelectField('Major by Academic Area', choices = [('Agricultural Sciences', 'Agricultural Sciences'),
        ('Art, Architecture, and Design', 'Art, Architecture, and Design'), ('Biological and Environmental Sciences', 'Biological and Environmental Sciences'),
        ('Business', 'Business'), ('Communication', 'Communication'), ('Cultural Studies and Foreign Languages', 'Cultural Studies and Foreign Languages'),
        ('Economics', 'Economics'), ('Education', 'Education'), ('Engineering and Computer Science', 'Engineering and Computer Science'),
        ('Health Sciences', 'Health Sciences'), ('History, Literature, and Philosophy', 'History, Literature, and Philosophy'),
        ('Music', 'Music'), ('Physical and Mathematical Sciences', 'Physical and Mathematical Sciences'), ('Pre-Professional Studies', 'Pre-Professional Studies'),
        ('Social Sciences', 'Social Sciences'), ('Sport and Fitness', 'Sport and Fitness')])
    cgpa = StringField('Cumulative GPA', validators=[DataRequired()])
    egd = StringField('Expected Graduation Date', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('The username already exists! Please use a different username.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('The email is already in use! Please use a different email.')
    
    def validate_phonenum(self, phonenum):
        phonenum = User.query.filter_by(phonenum=phonenum.data).first()
        if phonenum is not None:
            raise ValidationError('The phone number is already in use! Please use a different phone number.')

    def validate_wsuid(self, wsuid):
        wsuid = User.query.filter_by(wsuid=wsuid.data).first()
        if wsuid is not None:
            raise ValidationError('The WSU ID is already in use! Please use a different WSU ID.')


class ForTForm(FlaskForm):
    faculty = SubmitField('Faculty')
    TA = SubmitField('TA')

class editTAform(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    fullname = StringField('Full Name', validators=[DataRequired()])
    phonenum = StringField('Phone Number', validators=[DataRequired()])
    major = SelectField('Major by Academic Area', choices = [('Agricultural Sciences', 'Agricultural Sciences'),
        ('Art, Architecture, and Design', 'Art, Architecture, and Design'), ('Biological and Environmental Sciences', 'Biological and Environmental Sciences'),
        ('Business', 'Business'), ('Communication', 'Communication'), ('Cultural Studies and Foreign Languages', 'Cultural Studies and Foreign Languages'),
        ('Economics', 'Economics'), ('Education', 'Education'), ('Engineering and Computer Science', 'Engineering and Computer Science'),
        ('Health Sciences', 'Health Sciences'), ('History, Literature, and Philosophy', 'History, Literature, and Philosophy'),
        ('Music', 'Music'), ('Physical and Mathematical Sciences', 'Physical and Mathematical Sciences'), ('Pre-Professional Studies', 'Pre-Professional Studies'),
        ('Social Sciences', 'Social Sciences'), ('Sport and Fitness', 'Sport and Fitness')])
    cgpa = StringField('Cumulative GPA', validators=[DataRequired()])
    egd = StringField('Expected Graduation Date', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

class editfacform(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    fullname = StringField('Full Name', validators=[DataRequired()])
    phonenum = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

class CourseForm(FlaskForm):
    subject =  SelectField('Subject by Academic Area', choices = [('Agricultural Sciences', 'Agricultural Sciences'),
        ('Art, Architecture, and Design', 'Art, Architecture, and Design'), ('Biological and Environmental Sciences', 'Biological and Environmental Sciences'),
        ('Business', 'Business'), ('Communication', 'Communication'), ('Cultural Studies and Foreign Languages', 'Cultural Studies and Foreign Languages'),
        ('Economics', 'Economics'), ('Education', 'Education'), ('Engineering and Computer Science', 'Engineering and Computer Science'),
        ('Health Sciences', 'Health Sciences'), ('History, Literature, and Philosophy', 'History, Literature, and Philosophy'),
        ('Music', 'Music'), ('Physical and Mathematical Sciences', 'Physical and Mathematical Sciences'), ('Pre-Professional Studies', 'Pre-Professional Studies'),
        ('Social Sciences', 'Social Sciences'), ('Sport and Fitness', 'Sport and Fitness')])
    number = StringField('Course Number', validators=[DataRequired()])
    title = StringField('Course Title', validators=[DataRequired()])
    gpareq = StringField('GPA Requirement')
    prevgrade = StringField('Previous Grade Recieved')
    numslots = StringField('Number of TA Slots Available', validators=[DataRequired()])
    addinfo = StringField('Additional Info')
    submit = SubmitField('Create Course')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ApplyForm(FlaskForm):
    prevgrade = StringField('Your previous grade in this course (Write N/A if not applicable):', validators=[DataRequired()])
    whentaken = StringField('Year and Semester you took this course (Write N/A if not applicable):', validators=[DataRequired()])
    whenappfor = StringField("Year and Semester you're applying for:", validators=[DataRequired()])
    statement = StringField('Why are you right for this position?')
    submit = SubmitField('Apply')

class AssignForm(FlaskForm):
    courseid = IntegerField('Course ID', validators=[DataRequired()])
    assign = SubmitField('Assign')