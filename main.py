import os
from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user
from data import db_session
from data.models import User, Jobs
from forms import RegisterForm, LoginForm, AddJobForm

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route('/')
def works_log():
    return render_template('index.html', jobs=session.query(Jobs).all(),
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
    form = AddJobForm(data={'team_leader': current_user.id})
    if form.validate_on_submit():
        job = Jobs()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        session.add(job)
        session.commit()
        return redirect('/')
    return render_template('add_job.html', title='Adding a Job', form=form)


@app.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = session.query(Jobs).get(job_id)
    if job:
        if current_user.id == 1 or current_user.id == job.team_leader:
            form = AddJobForm(obj=job)
            if form.validate_on_submit():
                job.job = form.job.data
                job.team_leader = form.team_leader.data
                job.work_size = form.work_size.data
                job.collaborators = form.collaborators.data
                job.is_finished = form.is_finished.data
                session.commit()
                return redirect('/?message=Job saved&message_type=success')
            return render_template('add_job.html', title='Editing a Job', form=form)
        return redirect('/?message=You haven\'t permission for editing others '
                        'jobs!&message_type=danger')
    return redirect(f'/?message=Job with id {job_id} not found&message_type=danger')


if __name__ == '__main__':
    db_session.global_init('db/mars_explorer.sqlite')
    session = db_session.create_session()
    app.run(port=8080, host='127.0.0.1')
