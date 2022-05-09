from app import app, get_posts, create_post, session, get_post
from flask import render_template, request, redirect, make_response, flash
from posts.forms import PostForm, SearchForm
from data.__all_models import *
from data import db_session
from forms.user import RegisterForm
import time


@app.route("/mregister", methods=["GET", "POST"])
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    print(request.url_rule)
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Вы зарегистрированы. Пройдите на главную страницу.")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        response = make_response(redirect('/main_page'))
        response.set_cookie("id", str(user.id))
        return response
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/create", methods=["POST", "GET"])
def create_post():
    id_ = int(request.cookies.get("id", 0))
    if not id_:
        return make_response(redirect("/mregister"))
    form = PostForm()
    if request.method == "POST":
        s = db_session.create_session()
        post = Posts(title=request.form['title'],
                     content=request.form['body'],
                     author=id_)
        s.add(post)
        s.commit()
        return redirect("/posts")
    return render_template('create_post.html', form=form)


@app.route("/")
def redirect_():
    return redirect("/main_page")


@app.route('/main_page', methods=["POST", "GET"])
def index():
    id_ = int(request.cookies.get("id", 0))
    if not id_:
        return make_response(redirect("/mregister"))
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        text = request.form['url']
        s = db_session.create_session()
        post = s.query(Posts).filter(Posts.title.like(f"%{text}%")).first()
        if not post:
            return redirect("/posts")
        else:
            return redirect(f"/post/{post.id}")


@app.route('/posts')
def posts():
    id_ = int(request.cookies.get("id", 0))
    if not id_:
        return make_response(redirect("/mregister"))
    data = get_posts(session)
    return render_template("posts.html", posts=data)


@app.route('/post/<int:id>')
def post(id):
    id_ = int(request.cookies.get("id", 0))
    if not id_:
        return make_response(redirect("/mregister"))
    data = get_post(session, id)
    return render_template('post.html', post=data)
