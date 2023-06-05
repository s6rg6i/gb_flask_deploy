from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField, HiddenField


class LoginForm(FlaskForm):
    next = HiddenField("")
    login = StringField("Логин", [
        validators.Length(min=1, message='Поле "Логин" требует заполнения'), ])
    password = PasswordField("Пароль", [
        validators.Length(min=1, message='Поле "Пароль" требует заполнения'), ])
    submit = SubmitField('Авторизоваться')
    fields = ['next', 'login', 'password', 'submit']


class RegisterForm(FlaskForm):
    login = StringField("Логин", [
        validators.Length(min=1, message='Поле "Логин" требует заполнения'), ])
    name = StringField("Полное имя", [
        validators.Length(min=1, message='Поле ""Полное имя"" требует заполнения'), ])
    email = StringField("Е-мейл", [
        validators.Length(min=1, message='Поле "Е-мейл" требует заполнения'),
        validators.Email(message='Некорректный Е-мейл')], )
    password = PasswordField("Пароль", [
        validators.Length(min=1, message='Поле "Пароль" требует заполнения'),
        validators.EqualTo("confirm")], )
    confirm = PasswordField("Подтверждение пароля", [
        validators.Length(min=1, message='Поле "Подтверждение пароля" требует заполнения'), ])
    submit = SubmitField('Зарегистрироваться')
    fields = ['login', 'name', 'email', 'password', 'confirm', 'submit']
