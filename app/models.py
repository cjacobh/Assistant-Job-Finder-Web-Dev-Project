from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    status = db.Column(db.Integer, default = 0)        # For TA's: 0 = not accepted to course, anything other than 0 corresponds to course id accepted to 
    tof = db.Column(db.Integer)                        # tof stands for TA or Faculty, 1 = TA, 2 = Faculty
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique = True)
    phonenum = db.Column(db.String(20), unique = True)
    wsuid = db.Column(db.String(20), unique = True)
    password_hash = db.Column(db.String(128))
    major = db.Column(db.String(128))
    cgpa = db.Column(db.String(128))
    egd = db.Column(db.String(128))
    courses = db.relationship('Course', backref='professor')
    appsinuser = db.relationship('Apply', back_populates='_user')

    def __repr__(self):
        return 'User ID: {}\nUsername: {}\nUser Email: {}'.format(self.id, self.username, self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_applied(self, newclass):
        return self.courses.filter(Course.course_id == newclass.id).count() > 0
    
    def withdraw_app(self, newclass):
        if self.is_applied(newclass):
            self.courses.remove(newclass)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(128))
    number = db.Column(db.String(10))
    title = db.Column(db.String(128))
    gpareq = db.Column(db.Float)
    prevgrade = db.Column(db.String(4))
    numslots = db.Column(db.Integer)
    addinfo = db.Column(db.String(256))
    prof_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    appsincourse = db.relationship('Apply', back_populates='_course')

    def prof_exists(self, newprofessor):
        if self.prof_id != 0:
            self.course.remove(newprofessor)

class Apply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prevgrade = db.Column(db.String(10))
    whentaken = db.Column(db.String(30))
    whenappfor = db.Column(db.String(30))
    statement = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    _user = db.relationship('User')
    _course = db.relationship('Course')

db.create_all()
