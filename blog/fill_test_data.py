import pathlib

from werkzeug.security import generate_password_hash
from datetime import datetime

from blog import create_app
from blog.extension import db
from blog.models import User, Profile, Post, Category, Tag, Like, Comment, post_tag
import json


def db_tables_cleanup():
    """ Очистка таблиц БД """
    db.session.query(Comment).delete()
    db.session.query(Profile).delete()
    db.session.query(post_tag).delete()
    db.session.query(Tag).delete()
    db.session.query(Like).delete()
    db.session.query(Post).delete()
    db.session.query(Category).delete()
    db.session.query(User).delete()
    db.session.commit()


def db_tables_filling(file_name: str):
    """ Заполнение таблиц базы данных тестовыми данными """
    print(pathlib.Path.cwd())
    with open(file_name, encoding="utf8") as f:
        data_json = json.load(f)

    password = generate_password_hash('1')
    users = [User(login=u['login'], password=password, is_staff=u['is_staff'],
                  profile=Profile(name=u['name'], email=u['email'],
                                  birthday=datetime(*map(int, u['birthday'].split('-')))))
             for u in data_json['users']]
    db.session.add_all(users)

    categories = [Category(name=ctg) for ctg in data_json['categories']]
    db.session.add_all(categories)

    tags = [Tag(title=tag) for tag in data_json['tags']]
    db.session.add_all(tags)

    posts = [Post(title=post['title'], image=post['image'], content=post['content'],
                  user_id=post['user_id'], category_id=post['category_id'],
                  tags=[tags[i - 1] for i in post['tags']]
                  )
             for post in data_json['posts']]
    db.session.add_all(posts)

    likes = [Like(user_id=like['user_id'], post_id=like['post_id']) for like in data_json['likes']]
    db.session.add_all(likes)

    comments = []
    for art in data_json['comments']:
        for c in art["remark"]:
            parent = comments[c["comments_id"] - 1] if c["comments_id"] else None
            comments.append(Comment(text=c["text"], post_id=art["post_id"], user_id=c["user_id"], parent=parent))

    for comment in comments:
        comment.save()

    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.app_context().push()
    db_tables_cleanup()
    db_tables_filling('..\\data.json')
