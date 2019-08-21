from flask import Blueprint


bp = Blueprint('main', __name__)


from blog_app.main import routes
