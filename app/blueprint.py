from flask import Blueprint
from flask import render_template
from flask import request, url_for, redirect
from posts.forms import PostForm
from data import db_session
from data.__all_models import *


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def index():
    q = request.args.get('q')
    s = db_session.create_session()
    if q:
        post = s.query(Posts).filter(Posts.title.contains(q) | Posts.body.contains(q)).all()
    else:
        post = s.query(Posts).all()
    return render_template('search.html', posts=post)
