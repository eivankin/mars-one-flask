import os
from flask import Flask, render_template
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from data import db_session, jobs, users
from forms import RegisterForm

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')


@app.route('/')
def works_log():
    return render_template('works_log.html', jobs=session.query(jobs.Jobs).all())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if session.query(users.User).filter(users.User.email == form.login.data).first():
            return render_template('login.html', title='Регистрация', form=form,
                                   message='Login is not unique!', message_type='danger')
        user = users.User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.login.data
        user.hashed_password = generate_password_hash(form.password.data)
        session.add(user)
        session.commit()
        return render_template('login.html', title='Регистрация', form=form,
                               message='Account successfully created', message_type='success')
    return render_template('login.html', title='Регистрация', form=form)


if __name__ == '__main__':
    db_session.global_init('db/mars_explorer.sqlite')
    session = db_session.create_session()
    app.run(port=8080, host='127.0.0.1')
