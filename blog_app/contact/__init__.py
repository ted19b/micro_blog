from flask import Blueprint


bp = Blueprint('contact', __name__)


from blog_app.contact import contact_email, routes, forms