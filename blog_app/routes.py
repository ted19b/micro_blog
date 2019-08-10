from blog_app import app, db
from flask import render_template, flash, redirect, url_for, request

from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from blog_app.models import User
from blog_app.forms import LoginForm, RegistrationForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home Page')


@app.route('/dashboard')
@login_required
def dashboard():
    posts = [
        {
            'author': {'username': 'Youssoupha'},
            'body': 'great men are not born in greatness, but they grow'
        },
        {
            'author': {'username': 'Kery James'},
            'body': "I did it for myself, that's true, but I did it for you too, I did it for us"
        }
    ]
    return render_template('dashboard.html', title='Welcome to the Dashboard', posts=posts, user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Registration', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dashboard'))
