from flask import Blueprint

bp = Blueprint('errors', __name__)

from blog_app.errors import errors_handler
