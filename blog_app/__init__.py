import os
import logging

from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask, request, current_app
from flask_babel import Babel, lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import Config


# Creation of all extension instance

# for the database
db = SQLAlchemy()

# to make migration after change in database without lose data
migrate = Migrate()

# for language translation
babel = Babel()

# for login fonction
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')

# for mail support in the app
mail = Mail()

# Add twitter Bootstrap to the app
bootstrap = Bootstrap()

# Font awesome
fa = FontAwesome()

# flask moment to handle with date and time of the user
moment = Moment()


# The decorated function is invoked for each request to select a language translation to use for that request
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


def create_app(config_class=Config):
    # Creation of the application instance
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Registration of all extension to the app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    fa.init_app(app)

    # Registration of the Blueprint error, auth
    from blog_app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from blog_app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from blog_app.contact import bp as contact_bp
    app.register_blueprint(contact_bp)

    from blog_app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # to send a mail to a developper when an error occurs in the app
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='cyberusdev' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # save the log in the file
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


from blog_app import models
