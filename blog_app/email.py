from threading import Thread
from flask import render_template
from flask_mail import Message
from blog_app import mail, app
from blog_app.models import User


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user: User):
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))


def send_contact_mail(name, email, message):
    devmail = 'cyberusdev@gmail.com'
    send_email('[Microblog] Contact',
               sender=email,
               recipients=[devmail],
               text_body=render_template('email/contact_support.txt', name=name, email=email, message=message),
               html_body=render_template('email/contact_support.html', name=name, email=email, message=message))
