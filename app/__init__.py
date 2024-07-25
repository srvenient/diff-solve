__version__ = '0.1.0'


def create_app():
    from flask import Flask

    app = Flask(__name__)
    app.config.from_object('config.Config')

    from . import routes
    app.register_blueprint(routes.bp)

    return app
