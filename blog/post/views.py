import os

from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user

from blog.extension import db
from blog.fill_test_data import db_tables_cleanup, db_tables_filling
from blog.forms.post_forms import CreatePostForm, CommentForm
from blog.functions import render_with_common_dict, get_file_name
from blog.models import User, Profile, Post, Category, Tag, Like, Comment

post = Blueprint("post", __name__, static_folder="../static")


@post.route("/", methods=('GET',))
@post.route('/index', methods=('GET',))
def post_list():
    print(url_for('static', filename='main.css'))
    return render_with_common_dict("post/posts.html", posts=Post.query.all(), title='Все статьи')


@post.route("/<int:pk>", methods=('GET',))
def post_detail(pk: int):
    # Добавим лайк посту, если можно
    if request.args.get('like', ''):  # url типа: /3?like=1
        if current_user.is_authenticated:
            # проверка user, post -> 1 like
            if not Like.query.filter_by(post_id=pk, user_id=current_user.id).all():
                like = Like(post_id=pk, user_id=current_user.id)
                db.session.add(like)
                db.session.commit()

    comm_id = int(request.args.get('comment', '0'))  # url типа: /3?comment=120
    form = CommentForm()
    comments = []
    # проверка - есть ли комментарии
    cs = Comment.query.filter_by(post_id=pk).order_by(Comment.path)
    if cs:
        comments = [dict(id=c.id, level=f"margin-left: {40 * c.level()}px;", author=c.author.login,
                         date=c.timestamp, text=c.text, is_form=c.id == comm_id) for c in cs]

    print(comments)
    return render_with_common_dict("post/post_detail.html", post=Post.query.get(pk), form=form, comments=comments)


@post.route("/search", methods=('GET',))
def posts_by_phrase():
    phrase = request.args.get('search', '')
    if phrase:
        posts = Post.query.filter(Post.content.contains(phrase)).all()
        title = f'Статьи, содержащих <{phrase}>'
        return render_with_common_dict("post/posts.html", posts=posts, title=title)
    return redirect(url_for('post.post_list'))


@post.route("/ctg/<int:pk>", methods=('GET',))
def posts_by_category(pk: int):
    title = f'Статьи из категории <{Category.query.get(pk).name}>'
    return render_with_common_dict("post/posts.html", posts=Category.query.get(pk).posts, title=title)


@post.route("/tag/<int:pk>", methods=('GET',))
def posts_by_tag(pk: int):
    title = f'Статьи с тегом <{Tag.query.get(pk).title}>'
    return render_with_common_dict("post/posts.html", posts=Tag.query.get(pk).posts, title=title)


@post.route("/create", methods=('GET', 'POST'))
@login_required
def create_post():
    form = CreatePostForm(request.form)
    if request.method == "GET":
        return render_with_common_dict("post/create_post.html", form=form)
    if form.validate_on_submit():
        title = form.title.data.strip()
        content = form.content.data
        category = Category.query.get(int(form.category.data))
        file_name = None
        f = form.photo.data
        if f:
            f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], get_file_name(f.filename)))
        author = User.query.get(current_user.id)
        tags = [tag for tag in Tag.query.filter(Tag.id.in_(form.tags.data))]
        cur_post = Post(title=title, image=file_name, content=content, category=category, author=author, tags=tags)
        db.session.add(cur_post)
        db.session.commit()
        return redirect(url_for('post.post_list'))
    return render_with_common_dict("post/create_post.html", form=form)


@post.route("/fill", methods=('GET',))
def fill_in_tbl():
    db_tables_cleanup()
    db_tables_filling('data.json')
    return redirect(url_for('post.post_list'))


@post.route("/del", methods=('GET',))
def clear_tbl():
    db_tables_cleanup()
    return redirect(url_for('post.post_list'))
