import click
from werkzeug.security import generate_password_hash

from blog import create_app
from blog.extension import db

app = create_app()


@app.cli.command('set-superuser')
@click.argument("pk")
def set_superuser(pk):
    """ Команда создания суперпользователя """
    from blog.models import User
    with app.app_context():
        if user := User.query.get(pk):
            user.is_staff = True
            db.session.add(user)
            db.session.commit()
            print(f'User id={pk} login={user.login} is_staff={user.is_staff}')
        else:
            print(f'User id={pk} not found')

