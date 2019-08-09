from blog_app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    mock_user = {'username': 'Tedi-Bär'}
    posts = [
        {
            'author': {'username': 'Youssoupha'},
            'body': 'great men are not born in greatness, but they grow'
        },
        {
            'author': {'username': 'Kery James'},
            'body': "I did it for myself, that's true, but I did it for you too, I did it for us"
        }
    ]
    return render_template('home.html', posts=posts, user=mock_user)
