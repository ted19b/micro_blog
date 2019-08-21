from flask import flash, redirect, url_for, render_template
from blog_app.contact import bp
from blog_app.contact.contact_email import send_contact_mail
from blog_app.contact.forms import ContactForm
from flask_babel import _


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_contact_mail(form.name.data, form.email.data, form.message.data)
        flash(_('your message has been correctly sent'), 'success')
        return redirect(url_for('contact.contact'))
    return render_template('contact.html', title='Contact Us', form=form)
