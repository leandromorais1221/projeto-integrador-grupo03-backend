from flask import Flask
from .models import *

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    from .config.extensions import cors
    cors.init_app(app)

    from .config.extensions import swagger
    swagger.init_app(app)

    from .config.extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from .config.extensions import jwt
    jwt.init_app(app)

    from .blueprints import auth, categories, transactions, reports
    app.register_blueprint(auth.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(transactions.bp)
    app.register_blueprint(reports.bp)

    from .cli import db_seed
    app.cli.add_command(db_seed)

    return app