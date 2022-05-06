from app import app, get_posts, create_post, session, get_post
from flask import render_template, request, redirect
from posts.forms import PostForm, SearchForm
from data.__all_models import *
from data import db_session


@app.route("/create", methods=["POST", "GET"])
def create_post():
    form = PostForm()
    if request.method == "POST":
        s = db_session.create_session()
        post = Posts(title=request.form['title'], content=request.form['body'])
        s.add(post)
        s.commit()
        return redirect("/posts")
    return render_template('create_post.html', form=form)


@app.route('/', methods=["POST", "GET"])
def index():
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
    data = get_posts(session)
    return render_template("posts.html", posts=data)


@app.route('/post/<int:id>')
def post(id):
    data = get_post(session, id)
    return render_template('post.html', post=data)
