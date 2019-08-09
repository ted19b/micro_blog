from flask import Flask

app = Flask(__name__)

from blog_app import routes
