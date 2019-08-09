from blog_app import app
from flask import render_template, flash, redirect, url_for

from blog_app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    mock_user = {'username': 'Tedi-Bär'}
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
    return render_template('home.html', posts=posts, user=mock_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))

        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)