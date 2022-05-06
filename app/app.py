from flask import Flask
from blueprint import posts
from data import db_session
from data.__all_models import *


def create_post(s, author, title, content):
    if not s:
        return
    post = Posts()
    post.title = title
    post.content = content
    post.author = author
    s.add(post)
    s.commit()
    print(f"[LOG] Added a new post with id = {post.id}")


def get_posts(s):
    if not s:
        return
    all_posts = s.query(Posts).all()
    return all_posts


def delete_post(s, id):
    if not s:
        return
    s.query(Posts).filter(Posts.id == id).delete()
    return True


def get_post(s, id):
    if not s:
        return
    data = s.query(Posts).filter(Posts.id == id).first()
    return data


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.register_blueprint(posts, url_prefix='/blog')
db_session.global_init("db/blogs.sqlite")
session = db_session.create_session()
