from flask import render_template
from blog_app.email import send_email


def send_contact_mail(name, email, message):
    devmail = 'cyberusdev@gmail.com'
    send_email('[Microblog] Contact',
               sender=email,
               recipients=[devmail],
               text_body=render_template('email/contact_support.txt', name=name, email=email, message=message),
               html_body=render_template('email/contact_support.html', name=name, email=email, message=message))
