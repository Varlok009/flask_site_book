from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ajnd,asndk29jdiaskdnm29p01p1'

# app.jinja_env.globals.update(list=list)

menu = [{"title": "Home", "url": "/"},
        {"title": "Article", "url": "/article"},
        {"title": "New books", "url": "/new_books"},
        {"title": "Profile", "url": "/profile"},
        {"title": "Login", "url": "/login"},
        ]

@app.route('/')
def main_page():
    return render_template('home.html', title='Book worm', menu=menu)

@app.route('/profile')
def profile():
    return render_template('profile.html', title='Book worm', menu=menu)

if __name__ == "__main__":
    app.run(debug=True)
