from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from .swagger import SWAGGER_TEMPLATE
from flask_cors import CORS

cors = CORS()
swagger = Swagger(template=SWAGGER_TEMPLATE)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
