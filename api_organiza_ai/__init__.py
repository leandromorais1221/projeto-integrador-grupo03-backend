from flask import Flask
from .blueprints import transactions
from .models import *


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    from .extensions import cors
    cors.init_app(app)

    from .extensions import swagger
    swagger.init_app(app)

    from .extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from .extensions import jwt
    jwt.init_app(app)

    from .blueprints import auth, categories, transactions
    app.register_blueprint(auth.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(transactions.bp)

    return app