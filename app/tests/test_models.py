import unittest
from app import app, db
from app.models import User, Course, Apply

class UserModelCase(unittest, TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='cjacobh', fullname='Cole Hensley', email='cole@wsu.edu')
        u.set_password('coleiscool')
        self.assertFalse(u.check_password('colesux'))
        self.assertTrue(u.check_password('coleiscool'))

    def test_apply(self):
        course = Course(subject='Business', number='101', title='Intro to Business',
            gpareq=2.0, prevgrade='C-', numslots=4, addinfo='Need good students')
        db.session.add(course)
        db.session.commit()
        u = User(username='cjacobh', fullname='Cole Hensley', email='cole@wsu.edu')
        a = Apply(prevgrade='A', whentaken='Fall 2018', whenappfor='Spring 2021',
            statement='I like business')
        db.session.add(u)
        db.session.add(a)
        db.session.commit()
        self.assertEqual(u.appsinuser.all(), [])
        self.assertEqual(a.appsincourse.all(), [])

        u.Apply(a)
        db.session.commit()
        self.assertTrue(u.is_applied(a))
        self.assertEqual(u.appsinuser.count(), 1)
        self.assertEqual(u.appsinuser.first().coursenum, '355')
        self.assertEqual(u.appsinuser.first().major, 'CptS')
        self.assertEqual(a.appsincourse.count(), 1)
        self.assertEqual(a.appsincourse.first().username, 'john')

        u.withdraw_app(a)
        db.session.commit()
        self.assertFalse(u.is_applied(a))
        self.assertEqual(u.appsinuser.count(), 0)
        self.assertEqual(a.appsincourse.count(), 0)
    
    def test_course(self):
        course = Course(subject='Economics', number='101', title='Intro to Economics',
            gpareq=3.0, prevgrade='C', numslots=5, addinfo='Need hard working students')
        db.session.add(course)
        db.session.commit()
        u = User(tof  = 2, username='cjacobh', fullname='Cole Hensley', email='cole@wsu.edu', phonenum = '3601215278', wsuid = '12345678')
        c = Course(subject = 'Business', number='101', title='Intro to Business',
            gpareq=2.0, prevgrade='C-', numslots=4, addinfo='Need good students')
        
        db.session.add(u)
        db.session.add(c)
        db.session.commit()
        self.assertEqual(u.courses.all(), [])
        self.assertEqual(c.appsincourse.all(), [])

        self.assertTrue(c.prof_id > 0)
        self.assertEqual(c.subject, 'Business')
        self.assertEqual(c.number, '101')
    
    def test_TAuser(self):
        u = User(tof  = 1, username='cjacobh', fullname='Cole Hensley', email='cole@wsu.edu', phonenum = '3601215278', wsuid = '12345678')
        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.tof, 1)
        self.assertEqual(u.username, 'cjacobh')
        self.assertEqual(u.fullname, 'Cole Hensley')

    def test_Facuser(self):
        u = User(tof  = 2, username='cjacobh', fullname='Cole Hensley', email='cole@wsu.edu', phonenum = '3601215278', wsuid = '12345678')
        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.tof, 2)
        self.assertEqual(u.username, 'cjacobh')
        self.assertEqual(u.fullname, 'Cole Hensley')



