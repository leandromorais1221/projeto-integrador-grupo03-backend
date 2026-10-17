from flask import Flask, jsonify
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

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "Token inválido ou ausente"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Token inválido ou ausente"}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token inválido ou ausente"}), 401

    from .blueprints import helloworld
    app.register_blueprint(helloworld.bp)

    from .blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app