from flask import Flask, render_template, request, url_for, session, redirect, abort, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlite3
import os
from FDataBase import FDataBase
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm

BATABASE = 'site.db'
DEBUG = True
SECRET_KEY = 'ajnd,asndk29jdiaskdnm29p01p1'

# app.jinja_env.globals.update(list=list)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'site.db')))

title = "Worm book"
menu = [{"title": "Home", "url": "/"},
        {"title": "Posts", "url": "/posts"},
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


login_manager = LoginManager(app)


dbase = None
@app.before_request
def before_request():
    """Соединяет с БД перед обработкой запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    print(user_id)
    return UserLogin().fromDB(user_id, dbase)


def get_db():
    """Устанавливает соединение с БД"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


def connect_db():
    """Подключает к БД"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.teardown_appcontext
def close_db(error):
    """Закрывает соединение с БД"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404Error.html', title=title, menu=dbase.getMenu(), soc_links=soc_links)


@app.errorhandler(401)
def no_authenticated(error):
    return render_template('401Error.html', title=title, menu=dbase.getMenu(), soc_links=soc_links)


@app.route('/')
def index():
    return render_template('index.html', title=title, menu=dbase.getMenu(), soc_links=soc_links, posts=dbase.getPost())


@app.route('/profile')
@login_required
def profile_none():
    return redirect(url_for('profile', username=current_user.get_id()))


@app.route('/profile/<username>', methods=["POST", "GET"])
@login_required
def profile(username):
    if request.method == "POST" and request.form:
        add_post()
    if username == str(current_user.get_id()):
        return render_template('profile.html', title=title, menu=dbase.getMenu(), soc_links=soc_links, username=current_user.get_id(), posts=dbase.getUserPost(current_user.get_id()))
    else:
        redirect('login')


def add_post():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        print(current_user.get_id())
        if len(request.form['article']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(current_user.get_id(), request.form['article'], request.form['book'], request.form['author'],
                                request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if current_user.get_id():
        return redirect(url_for('profile_none'))

    if form.validate_on_submit():
        user = dbase.getUserEmail(request.form['email'])
        if user and check_password_hash(user['psw'], form.password.data):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(request.args.get("next") or url_for("profile_none"))

        flash("Неверная пара логин/пароль", "error")

    return render_template('login.html', title=title, soc_links=soc_links, menu=dbase.getMenu(), form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('index'))


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # session.pop('_flashes', None)
        hash_psw = generate_password_hash(request.form['password'])
        res = dbase.addUser(request.form['name'], request.form['email'], hash_psw)
        if res:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", "error")

    return render_template('register.html', title=title, soc_links=soc_links, menu=dbase.getMenu(), form=form)


@app.route("/posts")
@login_required
def posts():
    return render_template('posts.html', title=title, soc_links=soc_links, menu=dbase.getMenu(), posts=dbase.getPost())


@app.route("/post/<int:post_id>")
def show_post(post_id):
    return render_template('post.html', title=title, post_id=post_id, soc_links=soc_links, menu=dbase.getMenu(), posts=dbase.getPost(
        post_id))


def create_db():
    """Создает таблицы в на основании скрипта"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


if __name__ == "__main__":
    app.run(debug=True)
