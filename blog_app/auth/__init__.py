from flask import Blueprint


bp = Blueprint('auth', __name__)


from blog_app.auth import routes
