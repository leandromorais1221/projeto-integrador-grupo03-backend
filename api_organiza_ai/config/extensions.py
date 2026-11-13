from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from .swagger import SWAGGER_CONFIG
from flask_cors import CORS
from .cors import CORS_CONFIG

cors = CORS(resources=CORS_CONFIG)
swagger = Swagger(template=SWAGGER_CONFIG)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()