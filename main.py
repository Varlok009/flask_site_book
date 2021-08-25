import time

from flask import Flask, render_template, request, url_for, session, redirect, abort, g, flash
import sqlite3
import os
from FDataBase import FDataBase

BATABASE = 'site.db'
DEBUG = True
SECRET_KEY = 'ajnd,asndk29jdiaskdnm29p01p1'

# app.jinja_env.globals.update(list=list)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'site.db')))

title = "Worm book"
menu = [{"title": "Home", "url": "/"},
        {"title": "Article", "url": "/article"},
        {"title": "New books", "url": "/new_books"},
        {"title": "Profile", "url": "/profile"},
        {"title": "Login", "url": "/login"},
        ]

soc_links = [{"alt": "F", "icon": "static/images/social-iconc/fb.PNG", "url": "/"},
             {"alt": "T", "icon": "static/images/social-iconc/tw.PNG", "url": "/"},
             {"alt": "P", "icon": "static/images/social-iconc/p.PNG", "url": "/"},
             {"alt": "G", "icon": "static/images/social-iconc/g/google.PNG", "url": "/"},
             {"alt": "I", "icon": "static/images/social-iconc/i/inst.PNG", "url": "/"},
             ]


@app.route('/')
def main_page():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('home.html', title=title, menu=dbase.getMenu(), soc_links=soc_links)


@app.route('/profile')
def profile_none():
    if 'userLogged' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('profile', username=session['userLogged']))


@app.route('/profile/<username>')
def profile(username):
    db = get_db()
    dbase = FDataBase(db)
    if 'userLogged' not in session or session['userLogged'] != username:
        return redirect(url_for('login'))

    return render_template('profile.html', title=title, menu=dbase.getMenu(), soc_links=soc_links, username=username)


@app.route("/login", methods=["POST", "GET"])
def login():
    db = get_db()
    dbase = FDataBase(db)
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "var" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=dbase.getMenu())


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Создает таблицы в на основании скрипта"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Устанавливает соединение с БД в момент запроса"""
    if not hasattr(g, 'link.db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    """Закрывает соединение с БД"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/add_article", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['article']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['article'], request.form['book'], request.form['author'], request.form['post'])
            time.sleep(1)
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return redirect(url_for('profile_none'))


@app.route("/articles")
def articles():
    db = get_db()
    dbase = FDataBase(db)

    return render_template('articles.html', title=title, menu=dbase.getMenu(), posts=dbase.getArticles())


if __name__ == "__main__":
    app.run(debug=True)
