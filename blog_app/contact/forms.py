from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from flask_babel import lazy_gettext as _l


class ContactForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    message = TextAreaField(_l('Message'), validators=[DataRequired(), Length(min=1, max=500)])
    send_message = SubmitField(_l('Send message'))
