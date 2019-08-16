from blog_app import app, db
from flask import render_template, flash, redirect, url_for, request

from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from blog_app.email import send_password_reset_email
from blog_app.models import User, Post
from blog_app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, \
    ResetPasswordForm, ContactForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home Page')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!', 'info')
        return redirect(url_for('dashboard'))

    # implement pagination in the dasboard page
    pagination = set_pagination(current_user, request)

    return render_template('dashboard.html', title='Welcome to the Dashboard', posts=pagination[0].items,
                           next_url=pagination[1], prev_url=pagination[2], user=current_user, form=form)


# show the posts with pagination
def set_pagination(actual_user, actual_request_param):
    page = actual_request_param.args.get('page', 1, type=int)
    posts = actual_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('dashboard', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('dashboard', page=posts.prev_num) if posts.has_prev else None

    return posts, next_url, prev_url


@app.route('/explore')
@login_required
def explore():
    # implement pagination in the dasboard page
    pagination = set_pagination(current_user, request)

    return render_template('dashboard.html', title='Explore', posts=pagination[0].items,
                           next_url=pagination[1], prev_url=pagination[2])


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        # if the user was redirected to the login page when he/she requested access to a another page
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
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Registration', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc())\
        .paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None

    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.edit_username.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('user', username=current_user.username))

    elif request.method == 'GET':
        form.edit_username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', avatar=current_user.avatar(350), title='Edit Profile', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dashboard'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username), 'warning')
        return redirect(url_for('dashboard'))
    if user == current_user:
        flash('You cannot follow yourself!', 'info')
        return redirect(url_for('user', username=username))

    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username), 'info')
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username), 'warning')
        return redirect(url_for('dashboard'))
    if user == current_user:
        flash('You cannot unfollow yourself!', 'info')
        return redirect(url_for('user', username=username))

    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username), 'info')
    return redirect(url_for('user', username=username))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)

        flash('Check your email for the instruction to reset your password', 'info')

        return redirect(url_for('login'))

    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    user = User.verify_reset_password_token(token)
    if not user:
        flash('Your token has expired, please restart the process', 'warning')
        return redirect(url_for('home'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been reset', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('your message has been correctly sent', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact Us', form=form)
