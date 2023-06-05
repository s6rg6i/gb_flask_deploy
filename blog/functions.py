import pathlib
from secrets import token_hex

from flask import render_template
import imghdr

from werkzeug.utils import secure_filename

from blog.models import Category, Tag


def render_with_common_dict(template, **context):
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template(template, **context, categories=categories, tags=tags)


def get_file_name(filename):
    f = pathlib.Path(secure_filename(filename))
    return f"{f.stem}_{token_hex(8)}{f.suffix}"


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    return imghdr.what(None, header)


if __name__ == '__main__':
    s0 = "out_23__1.txt"
    s1 = get_file_name(s0)
    print(s1)

    fff = lambda x: get_file_name(x)
    print(f'{fff(s0)=}')
