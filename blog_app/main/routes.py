from blog_app.main import bp
from blog_app import db
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from datetime import datetime
from flask_babel import _, get_locale
from guess_language import guess_language
from blog_app.models import User, Post
from blog_app.main.forms import EditProfileForm, PostForm, SearchForm


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/')
@bp.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    return render_template('home.html', title='Home Page')


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = PostForm()

    if form.validate_on_submit():
        # for automatic language translation... to be implemented
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'), 'info')
        return redirect(url_for('main.dashboard'))

    # implement pagination in the dasboard page
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.dashboard', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.dashboard', page=posts.prev_num) if posts.has_prev else None

    return render_template('dashboard.html', title=_('Dashboard'), form=form, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    # implement pagination in the explore page
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None

    return render_template('dashboard.html', title=_('Explore'), posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()) \
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) if posts.has_prev else None

    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.edit_username.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash(_('Your changes have been saved.'), 'success')
        return redirect(url_for('main.user', username=current_user.username))

    elif request.method == 'GET':
        form.edit_username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', avatar=current_user.avatar(350), title='Edit Profile', form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username), 'warning')
        return redirect(url_for('main.dashboard'))
    if user == current_user:
        flash(_('You cannot follow yourself!'), 'info')
        return redirect(url_for('main.user', username=username))

    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username), 'info')
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username), 'warning')
        return redirect(url_for('main.dashboard'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'), 'info')
        return redirect(url_for('main.user', username=username))

    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username), 'info')
    return redirect(url_for('main.user', username=username))


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total['value'] > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts, next_url=next_url, prev_url=prev_url)
