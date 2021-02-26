import os
import json
from flask import Flask, render_template, redirect, request, make_response, jsonify
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user
from data import db_session, jobs_api, users_api
from data.models import User, Jobs, Department, Category
from forms import RegisterForm, LoginForm, JobForm, DepartmentForm

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)


def save_job(form, job=None):
    flag = False
    if job is None:
        job = Jobs()
        flag = True
    job.job = form.job.data
    job.team_leader_id = form.team_leader_id.data
    job.work_size = form.work_size.data
    job.collaborators = form.collaborators.data
    job.is_finished = form.is_finished.data
    job.categories = session.query(Category).filter(
        Category.id.in_(json.loads(form.categories.data))).all()
    if flag:
        session.add(job)
    session.commit()


def save_department(form, department=None):
    flag = False
    if department is None:
        department = Department()
        flag = True
    department.title = form.title.data
    department.chief_id = form.chief_id.data
    department.members = form.members.data
    department.email = form.email.data
    if flag:
        session.add(department)
    session.commit()


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error=None):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found(error=None):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/')
def works_log():
    # Решил оправдать наличие категорий хоть каким-то функционалом
    category = request.args.get('category_id')
    if category:
        jobs = session.query(Category).get(category).jobs
    else:
        jobs = session.query(Jobs).all()
    return render_template('index.html', jobs=jobs,
                           title='Works log', message=request.args.get('message'),
                           message_type=request.args.get('message_type'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if session.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Login is not unique!', message_type='danger')
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.login.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return render_template('register.html', title='Register', form=form,
                               message='Account successfully created', message_type='success')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', title='Authorization', message_type='danger',
                               message='Invalid login or password', form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/add-job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm(data={'team_leader_id': current_user.id})
    if form.validate_on_submit():
        save_job(form)
        return redirect('/?message=Job added&message_type=success')
    return render_template('add_job.html', title='Adding a Job', form=form)


@app.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = session.query(Jobs).get(job_id)
    if job:
        if current_user.id == 1 or current_user.id == job.team_leader_id:
            form = JobForm(obj=job)
            if form.validate_on_submit():
                save_job(form, job)
                return redirect('/?message=Job saved&message_type=success')
            return render_template('add_job.html', title='Editing a Job', form=form)
        return redirect('/?message=You haven\'t permission for editing others '
                        'jobs!&message_type=danger')
    return redirect(f'/?message=Job with id "{job_id}" not found&message_type=danger')


@app.route('/delete-job/<int:job_id>')
@login_required
def delete_job(job_id):
    job = session.query(Jobs).get(job_id)
    if job:
        if current_user.id == 1 or current_user.id == job.team_leader_id:
            session.delete(job)
            session.commit()
            return redirect('/?message=Job deleted&message_type=success')
        return redirect('/?message=You haven\'t permission for deleting others '
                        'jobs!&message_type=danger')
    return redirect(f'/?message=Job with id "{job_id}" not found&message_type=danger')


@app.route('/departments')
def departments():
    return render_template('departments.html', title='Departments',
                           departments=session.query(Department).all(),
                           message=request.args.get('message'),
                           message_type=request.args.get('message_type'))


@app.route('/add-department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm(data={'chief_id': current_user.id})
    if form.validate_on_submit():
        save_department(form)
        return redirect('/departments?message=Department added&message_type=success')
    return render_template('add_department.html', title='Adding a Department', form=form)


@app.route('/edit-department/<int:dep_id>', methods=['GET', 'POST'])
@login_required
def edit_department(dep_id):
    department = session.query(Department).get(dep_id)
    if department:
        if current_user.id == 1 or current_user.id == department.chief_id:
            form = DepartmentForm(obj=department)
            if form.validate_on_submit():
                save_department(form, department)
                return redirect('/departments?message=Department saved&message_type=success')
            return render_template('add_department.html', title='Editing a Department', form=form)
        return redirect('/departments?message=You haven\'t permission for editing others '
                        'departments!&message_type=danger')
    return redirect(f'/departments?message=Department with id "{dep_id}" not found&message_type'
                    '=danger')


@app.route('/delete-department/<int:dep_id>')
@login_required
def delete_department(dep_id):
    department = session.query(Department).get(dep_id)
    if department:
        if current_user.id == 1 or current_user.id == department.chief_id:
            session.delete(department)
            session.commit()
            return redirect('/departments?message=Department deleted&message_type=success')
        return redirect('/departments?message=You haven\'t permission for deleting others '
                        'departments!&message_type=danger')
    return redirect(f'/departments?message=Department with id "{dep_id}" not found&message_type'
                    '=danger')


if __name__ == '__main__':
    db_session.global_init('db/mars_explorer.sqlite')
    session = db_session.create_session()
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
