from blog_app import app, db
from blog_app.models import User, Post
from blog_app import cli


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}