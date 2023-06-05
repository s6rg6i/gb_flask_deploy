from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, validators, SubmitField, TextAreaField, SelectField, SelectMultipleField

from blog.models import Category, Tag


class CreatePostForm(FlaskForm):
    title = StringField('Заголовок поста', [validators.Length(min=1, message='Поле "Заголовок" требует заполнения')])
    content = TextAreaField('Содержание поста', render_kw=dict(rows="9", cols="25"))
    category = SelectField('Выберите категорию поста')
    photo = FileField(validators=[FileAllowed(["png", "jpg", "jpeg", "webp", "gif"], "Тип файла не разрешен!", )], )
    tags = SelectMultipleField('Выберите теги', coerce=int)
    submit = SubmitField('Создать')
    fields = ['title', 'content', 'category', 'photo', 'tags', 'submit']

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(ctg.id, ctg.name) for ctg in Category.query.all()]
        self.tags.choices = [(tag.id, tag.title) for tag in Tag.query.all()]


class CommentForm(FlaskForm):
    content = TextAreaField('Ваш комментарий', render_kw=dict(rows="5", cols="50", autofocus=True))
    submit = SubmitField('Отправить')
    fields = ['content', 'submit']
