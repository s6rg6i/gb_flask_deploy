from flask import Flask, url_for

from blog import config, extension


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config.DevConfig)  # environment: BaseConfig, DevConfig, TestConfig
    print(app.config)
    register_extensions(app)  # register db
    register_blueprints(app)  # register Blueprints
    # register_commands(app)  # register console commands
    return app


def register_extensions(app: Flask):
    extension.db.init_app(app)

    extension.migrate.init_app(app, extension.db, compare_type=True)

    extension.login_manager.login_view = 'auth.login'
    extension.login_manager.init_app(app)

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    extension.admin.init_app(app)


def register_blueprints(app: Flask):
    """ Регистрация блюпринтов """
    from blog.auth.views import auth
    from blog.post.views import post
    from blog.user.views import user
    import blog.admin.views
    [app.register_blueprint(bp) for bp in (user, post, auth)]
