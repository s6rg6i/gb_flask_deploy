import os
import pathlib

from flask import url_for, redirect
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user
from markupsafe import Markup
from sqlalchemy import inspect

from blog.functions import get_file_name
from blog.models import User, Profile, Post, Category, Tag, Like
from blog.extension import admin, db


class CustomAdminView(ModelView):
    column_display_pk = True  # Разрешаем вывод id
    column_hide_backrefs = False  # Разрешаем вывод внешних ключей
    can_create = True
    can_edit = True
    can_delete = True

    def create_blueprint(self, adm):
        blueprint = super().create_blueprint(adm)
        blueprint.name = f'{blueprint.name}_admin'
        return blueprint

    def get_url(self, endpoint, **kwargs):
        if not (endpoint.startswith('.') or endpoint.startswith('admin.')):
            endpoint = endpoint.replace('.', '_admin.')
        return super().get_url(endpoint, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_staff

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class UserAdminView(CustomAdminView):
    column_exclude_list = ('password',)  # убираем отображение поля 'password'
    column_details_exclude_list = ('password',)
    column_export_exclude_list = ('password',)


class ProfileAdminView(CustomAdminView):
    # Подключаем отображение всех полей (и внешнего ключа user_id)
    column_list = [c_attr.key for c_attr in inspect(Profile).mapper.column_attrs]


class CategoryAdminView(CustomAdminView):
    ...


class TagAdminView(CustomAdminView):
    ...


file_path = pathlib.Path.cwd()


def prefix_name(obj, file_data):
    return get_file_name(file_data.filename)


class PostAdminView(CustomAdminView):
    # Подключаем отображение всех полей (и внешних ключей user_id, category_id)
    column_list = [c_attr.key for c_attr in inspect(Post).mapper.column_attrs]

    column_default_sort = ('title', True)
    column_sortable_list = ('id', 'author', 'title', 'tags', 'category')
    column_searchable_list = ['title', 'content']
    column_filters = ['title', User.login, 'tags']
    column_editable_list = ['title']

    def path_image(self, context, model, name):
        if not model.image:
            return ''
        url = url_for('static', filename=f'storage/{model.image}')
        return Markup(f'<img src="{url}" width="100">')

    form_extra_fields = {
        "image": form.ImageUploadField(
            'Image',
            base_path=os.path.join(file_path, 'blog/static/storage'),
            url_relative_path='storage',
            namegen=prefix_name,
            allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'gif', 'webp'],
            max_size=(1200, 780, True),
            thumbnail_size=(100, 100, True),
        )}

    column_formatters = {
        'image': path_image
    }


class LikeAdminView(CustomAdminView):
    # Подключаем отображение всех полей (и внешних ключей user_id, post_id)
    column_list = [c_attr.key for c_attr in inspect(Like).mapper.column_attrs]


# Добавляем views в админ панель (Для группы меню 'Models'-> category='Models')
[admin.add_view(view(model, db.session, name=name))
 for view, model, name in [
     (UserAdminView, User, 'Пользователи'), (ProfileAdminView, Profile, 'Профили'), (PostAdminView, Post, 'Статьи'),
     (CategoryAdminView, Category, 'Категории'), (TagAdminView, Tag, 'Теги'), (LikeAdminView, Like, 'Лайки')]]

# Добавляем exit в админ панель
admin.add_link(MenuLink(name='Exit', category='', url="/"))
