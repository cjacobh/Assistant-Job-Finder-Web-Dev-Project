import sys
from app import app,db
from sqlalchemy.sql.expression import update
from flask import render_template, flash, redirect, url_for, request
from flask_sqlalchemy import sqlalchemy
from flask_login import current_user, login_user, logout_user, login_required
from wtforms.validators import ValidationError


from app.forms import UserForm, LoginForm, editTAform, editfacform, CourseForm, ApplyForm, ForTForm, AssignForm
from app.models import User, Course, Apply

@app.route('/ForT', methods=["GET", "POST"])
def ForT():
    form = ForTForm()
    return render_template('ForT.html', title='Faculty or TA', form=form)

@app.route('/registerfac', methods=["GET", "POST"])
def registerfac():
    form = UserForm()
    if form.is_submitted():   ## change to validate_on_submit()
        user = User(tof=2, username=form.username.data, fullname=form.fullname.data, email = form.email.data, phonenum = form.phonenum.data, wsuid = form.wsuid.data,
            major = None, cgpa = None, egd = None)
        user.set_password(form.password.data)
        try:
            form.validate_username(form.username)
        except ValidationError:
            flash("Username already in use!")
            return redirect(url_for('registerfac'))
        try:
            form.validate_email(form.email)
        except ValidationError:
            flash("Email already in use!")
            return redirect(url_for('registerfac'))
        try:
            form.validate_phonenum(form.phonenum)
        except ValidationError:
            flash("Phone number already in use!")
            return redirect(url_for('registerfac'))
        try:
            form.validate_wsuid(form.wsuid)
        except ValidationError:
            flash("WSU ID already in use!")
            return redirect(url_for('registerfac'))
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you now have a Faculty account on the TA Course Finder!")
        return redirect(url_for('login'))
    return render_template('registerfac.html', title='Faculty Registration', form=form)

@app.route('/registerTA', methods=["GET", "POST"])
def registerTA():
    form = UserForm()
    if form.is_submitted():   ## change to validate_on_submit()
        user = User(tof=1, username=form.username.data, fullname=form.fullname.data, email = form.email.data, phonenum = form.phonenum.data, wsuid = form.wsuid.data,
            major = form.major.data, cgpa = form.cgpa.data, egd = form.egd.data)
        user.set_password(form.password.data)
        try:
            form.validate_username(form.username)
        except ValidationError:
            flash("Username already in use!")
            return redirect(url_for('registerTA'))
        try:
            form.validate_email(form.email)
        except ValidationError:
            flash("Email already in use!")
            return redirect(url_for('registerTA'))
        try:
            form.validate_phonenum(form.phonenum)
        except ValidationError:
            flash("Phone number already in use!")
            return redirect(url_for('registerTA'))
        try:
            form.validate_wsuid(form.wsuid)
        except ValidationError:
            flash("WSU ID already in use!")
            return redirect(url_for('registerTA'))
        db.session.add(user)        
        db.session.commit()
        flash("Congratulations, you now have a TA account on the TA Course Finder!")
        return redirect(url_for('login'))
    return render_template('registerTA.html', title='TA Registration', form=form)


@app.route("/login", methods = ["GET", "POST"])
def login():
    
    if current_user.is_authenticated and current_user.tof == 1:
        return redirect(url_for('index'))
    if current_user.is_authenticated and current_user.tof == 2:
        return redirect(url_for('Facindex'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.get_password(form.password.data):
            flash('Invalid Username or Password!')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        if current_user.tof == 1:
            return redirect(url_for('index'))
        elif current_user.tof == 2:
            return redirect(url_for('Facindex'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/", methods = ["GET", "POST"])
@app.route("/index", methods = ["GET", "POST"])
@login_required
def index():
    if current_user.tof == 2:
        return redirect(url_for('Facindex'))
    elif current_user.status != 0:
        return redirect(url_for('accepted'))
    else:
        form = ApplyForm()
        reccoursess = Course.query.filter(Course.subject.like(current_user.major)) 
        coursess = Course.query.order_by(Course.title)
        reccourses = reccoursess.all()
        courses = coursess.all()

        for app in current_user.appsinuser:
            for crs in courses:
                if app in crs.appsincourse:
                    courses.remove(crs)
        for app in current_user.appsinuser:
            for crs in reccourses:
                if app in crs.appsincourse:
                    reccourses.remove(crs)

        for crs in courses:
            if crs.numslots < 1:
                courses.remove(crs)
        for crs in reccourses:
            if crs.numslots < 1:
                reccourses.remove(crs)

        return render_template("index.html", title='TA Homepage', courses=courses, reccourses=reccourses, form=form)

@app.route('/accepted', methods = ['GET', 'POST'])
@login_required
def accepted():
    if current_user.tof == 2:
        return redirect(url_for('Facindex'))
    elif current_user.status == 0:
        return redirect(url_for('index'))
    else:
        crs = Course.query.filter_by(id=current_user.status).first()
        return render_template('accepted.html', title='You are a TA!', crs=crs)

@app.route('/leavecourse', methods = ['GET', 'POST'])
def leavecourse():
    if current_user.status != 0:
        current_user.status = 0
        db.session.commit()
        flash('You have removed yourself from the course, and can now apply for other courses.')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/Facindex', methods = ['GET', 'POST'])
@login_required
def Facindex():
    if current_user.tof == 1:
        return redirect(url_for('index'))
    else:    
        form = ApplyForm()
        idlist = []
        for course in Course.query.filter_by(prof_id = current_user.id):  ## creates sqlObj of courses made by current professor
            idlist.append(course.id)
        applications = Apply.query.filter(Apply.course_id.in_(idlist))

        return render_template('Facindex.html', title='Faculty Homepage', applications = applications.all(), form=form)

@app.route('/apply/<course_id>', methods = ['GET', 'POST'])
def apply(course_id):
    form = ApplyForm()
    courseobj = Course.query.filter_by(id = course_id).first()
    if form.validate_on_submit():
        application = Apply(prevgrade = form.prevgrade.data, whentaken = form.whentaken.data, whenappfor = form.whenappfor.data,
            statement = form.statement.data, _user = current_user, _course = courseobj)
        db.session.add(application)
        db.session.commit()
        flash("You have successfully applied to a TA position!")
        return redirect(url_for('index'))
    return render_template('apply.html', title='Application Page', courseobj=courseobj, form=form)

@app.route('/viewapps', methods = ['GET', 'POST'])
@login_required
def viewapps():
    if current_user.tof == 2:
        return redirect(url_for('Facindex'))
    else:
        form = ApplyForm()
        myapps = Apply.query.filter_by(user_id = current_user.id)
    return render_template('viewapps.html', title='View Applications', myapps=myapps.all(), form=form)

@app.route('/updateapp/<app_id>', methods = ['GET', 'POST'])
@login_required
def updateapp(app_id):
    if current_user.tof == 2:
        return redirect(url_for('Facindex'))
    else:
        form = ApplyForm()
        app = Apply.query.filter_by(id = app_id).first()
        if form.validate_on_submit():
            app.prevgrade = form.prevgrade.data
            app.whentaken = form.whentaken.data
            app.whenappfor = form.whenappfor.data
            app.statement = form.statement.data
            db.session.commit()
            flash("You have updated an application!")
            return redirect(url_for('viewapps'))
        elif request.method == 'GET':
            form.prevgrade.data = app.prevgrade
            form.whentaken.data = app.whentaken
            form.whenappfor.data = app.whenappfor
            form.statement.data = app.statement
    return render_template('updateapp.html', title='Update Application', app=app, form=form)

@app.route('/deleteapp/<app_id>', methods = ['GET', 'POST', 'DELETE'])
@login_required
def deleteapp(app_id):
    app = Apply.query.filter_by(id = app_id).first()
    db.session.delete(app)
    db.session.commit()
    flash('You have successfully deleted your application.')
    return redirect(url_for('viewapps'))

@app.route('/accept/<app_id>', methods = ['GET', 'POST', 'DELETE'])
@login_required
def accept(app_id):
    if current_user.tof == 1:
        return redirect(url_for('index'))
    else:
        app = Apply.query.filter_by(id = app_id).first()
        ta = User.query.filter_by(id = app._user.id).first()
        crs = Course.query.filter_by(id = app._course.id).first()
        ta.status = app._course.id
        crs.numslots = crs.numslots - 1
        db.session.delete(app)
        db.session.commit()
        for remapps in ta.appsinuser:
            db.session.delete(remapps)
            db.session.commit()
        flash('You have accepted a TA to your course!')
    return redirect(url_for('Facindex'))

@app.route('/deny/<app_id>', methods = ['GET', 'POST', 'DELETE'])
@login_required
def deny(app_id):
    if current_user.tof == 1:
        return redirect(url_for('index'))
    else:
        app = Apply.query.filter_by(id = app_id).first()
        db.session.delete(app)
        db.session.commit()
        flash('You have denied an application.')
    return redirect(url_for('Facindex'))

@app.route('/managecourses', methods = ['GET', 'POST', 'DELETE'])
@login_required
def managecourses():
    if current_user.tof == 1:
        return redirect(url_for('index'))
    else:
        students = User.query.filter(User.status == 0, User.tof == 1).all()
        tas = User.query.filter(User.status>0).all()
        courses = Course.query.filter_by(prof_id = current_user.id).all()
        return render_template('managecourses.html', title='Manage Courses', students=students,
            tas=tas, courses=courses)

@app.route('/editcourse/<course_id>', methods = ['GET', 'POST'])
@login_required
def editcourse(course_id):
    if current_user.tof == 1:
        return redirect(url_for('index'))
    else:
        form = CourseForm()
        course = Course.query.filter_by(id=course_id).first()
        if form.validate_on_submit():
            course.subject = form.subject.data
            course.number = form.number.data
            course.title = form.title.data
            course.gpareq = form.gpareq.data
            course.prevgrade = form.prevgrade.data
            course.numslots = form.numslots.data
            course.addinfo = form.addinfo.data
            db.session.commit()
            flash("You have updated your course!")
            return redirect(url_for('managecourses'))
        elif request.method == 'GET':
            form.subject.data = course.subject
            form.number.data = course.number
            form.title.data = course.title
            form.gpareq.data = course.gpareq
            form.prevgrade.data = course.prevgrade
            form.numslots.data = course.numslots
            form.addinfo.data = course.addinfo
        return render_template('editcourse.html', title='Edit Course', form=form, course=course)

@app.route('/deletecourse/<course_id>', methods = ['GET', 'POST', 'DELETE'])
@login_required
def deletecourse(course_id):
    if current_user.tof == 1:
        return redirect(url_for('index'))
    else:
        course = Course.query.filter_by(id = course_id).first()
        for apps in course.appsincourse:
            db.session.delete(apps)
            db.session.commit()
        for ta in User.query.all():
            if ta.status == course.id:
                ta.status = 0
        db.session.delete(course)
        db.session.commit()
        flash('You have successfully deleted this course, along with all applications within it.')
        flash("If any TA's had been accepted to assist this course, they have been removed from the course as well.")
        return redirect(url_for('managecourses'))
        
@app.route('/assign/<user_id>', methods = ['GET', 'POST', 'DELETE'])
@login_required
def assign(user_id):
    if current_user.tof == 1:
        return redirect(url_for('index'))
    else:
        form = AssignForm()
        student = User.query.filter_by(id=user_id).first()
        idlist = []
        for crs in Course.query.filter_by(prof_id = current_user.id):
            idlist.append(crs.id)
        profcourses = Course.query.filter(Course.id.in_(idlist))
        course = Course.query.filter_by(id = form.courseid.data).first()
        if form.validate_on_submit():
            if form.courseid.data in idlist:
                student.status = form.courseid.data
                course.numslots = course.numslots - 1
                for apps in student.appsinuser:
                    db.session.delete(apps)
                    db.session.commit()
                flash('You have assigned a student to your course!')
                db.session.commit()
                return redirect(url_for('managecourses'))
            else:
                flash('Must assign student to one of your courses!')
                return redirect(url_for('managecourses'))
        elif request.method == 'GET':
            form.courseid.data = student.status
    return render_template('assign.html', title='Assign TA', profcourses=profcourses.all(), student=student, form=form)


@app.route("/editTA", methods = ["GET", "POST"])
@login_required
def editTA():
    if current_user.tof == 2:
        return redirect(url_for('Facindex'))
    else:
        form = editTAform()
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.fullname = form.fullname.data
            current_user.phonenum = form.phonenum.data
            current_user.major = form.major.data
            current_user.cgpa = form.cgpa.data
            current_user.egd = form.egd.data
            db.session.commit()
            flash("You have updated your profile!")
            return redirect(url_for('index'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.fullname.data = current_user.fullname
            form.phonenum.data = current_user.phonenum
            form.major.data = current_user.major
            form.cgpa.data = current_user.cgpa
            form.egd.data = current_user.egd
        return render_template('editTA.html', title='Edit Profile', form=form)

@app.route("/editfac", methods = ["GET", "POST"])
@login_required
def editfac():
    if current_user.tof == 1:
        return redirect(url_for('index'))
    else:
        form = editfacform()
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.fullname = form.fullname.data
            current_user.phonenum = form.phonenum.data
            db.session.commit()
            flash("You have updated your profile!")
            return redirect(url_for('Facindex'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.fullname.data = current_user.fullname
            form.phonenum.data = current_user.phonenum
        return render_template('editfac.html', title='Edit Profile', form=form)

@app.route("/addcourse", methods = ['GET', 'POST'])
@login_required
def addcourse():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(subject = form.subject.data, number = form.number.data,
            title = form.title.data, gpareq = form.gpareq.data,
            prevgrade = form.prevgrade.data, numslots = form.numslots.data,
            addinfo = form.addinfo.data, professor = current_user)
        db.session.add(course)
        db.session.commit()
        flash("You have created a new course!")
        return redirect(url_for('Facindex'))
    return render_template('addcourse.html', title='Create Course', form=form)
