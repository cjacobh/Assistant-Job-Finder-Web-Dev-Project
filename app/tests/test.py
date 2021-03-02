import os
import temfile
import pytest
from config import basedir
from app import app, db, login
from app.models import user, course, apply

@pytest.fixture(scope='module')
def test_client(request):
    #re-configure the app for tests
    app.config.update(
        SECRET_KEY = 'bad-bad-key',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        WTF_CSRF_ENABLED = False,
        DEBUG = True,
        TESTING = True,
    )
    db.init_app(app)
    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()
 
    yield testing_client #testing
 
    ctx.pop()

@pytest.fixture
def init_database(request, test_client):
    db.create_all()
    if user.query.count() == 0:
        user1 = User(status=0, tof=2, username='jim', fullname='Jimothy Morris', email='jimothy@wsu.edu', phonenum=2222222222, wsuid=22222222, major='', cgpa='', edg=''))
        user.set_password('pass123')
        user2 = User(status=0, tof=1, username='jane', fullname='jane Doe', email='janedoe@wsu.edu', phonenum=1111111111, wsuid=11111111, major='Engineering and Computer Science', cgpa='3.5', edg='June 2020'))
        user2.set_password('jane123')
        db.session.add(user1)
        db.session.add(user1)
        db.session.commit()

    if course.query.count() == 0:
        db.session.add(Course(subject='Engineering and Computer Science', number=101, title='intro to cs', gpareq=3.0, prevgrade=3.3, numslots=15, addinfo='Be good with cs', prof_id=1))
        db.session.add(Course(subject='Music', number=162, title='music history', gpareq=2.7, prevgrade=3.0, numslots=2, addinfo='You must be exceptionally musical', prof_id=1))
        db.session.add(Course(subject='Engineering and Computer Science', number=102, title='advanced cs', gpareq=3.0, prevgrade=3.3, numslots=5, addinfo='5 years of industry experience required', prof_id=1))
        db.session.commit()

    yield

    db.drop_all()

def test_registerTA_page(request, test_client):
    response = test_client.get('.register')
    assert response.status_code == 200
    assert b"register" in response.data

def test_registerTA(request, test_client, initdatabase):
     response = test_client.post('/register', data=dict(status=0, tof=1, username='stu', fullname='stu dent', 
                                                        email='student@wsu.edu', phonenum=33333333333, wsuid=33333333, 
                                                        major='Engineering and Computer Science', cgpa='3.5', edg='June 2020')
    assert response.status_code == 200

    s = db.session.query.Student.filter(username='stu')
    assert s.first().email == 'student@wsu.edu'
    assert s.count() == 1
    assert b"Congratulations, you now have a TA account on the TA Course Finder!" in response.data

def test_registerFac_page(request, test_client):
    response = test_client.get('.register')
    assert response.status_code == 200
    assert b"register" in response.data

def test_registerFac(request, test_client, initdatabase):
     response = test_client.post('/register', data=dict(status=0, tof=2, username='pro', fullname='pro fessor', 
                                                        email='professor@wsu.edu', phonenum=4444444444, wsuid=44444444, 
                                                        major='Engineering and Computer Science', cgpa='', edg='')
    assert response.status_code == 200

    s = db.session.query.Faculty.filter(username=='pro fessor')
    assert s.first().email == 'professor@wsu.edu'
    assert s.count() == 1
    assert b"Congratulations, you now have a Faculty account on the TA Course Finder!" in response.data

