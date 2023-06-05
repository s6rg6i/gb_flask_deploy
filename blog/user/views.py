from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from blog.functions import render_with_common_dict
from blog.models import User

user = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@user.route("/")
def user_list():
    return render_with_common_dict("user/users.html", users=User.query.all())


@user.route("/<int:pk>")
def user_detail(pk: int):
    return render_with_common_dict("user/user_detail.html", user=User.query.get(pk))
