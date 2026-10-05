from flask import Blueprint

bp = Blueprint('hello', __name__)

@bp.get('/')
def hello():
    """
    Retorna uma mensagem de boas-vindas.
    ---
    tags:
      - Hello World
    responses:
      200:
        description: Mensagem retornada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: Hello, World!
    """
    return {
        'data': 'Hello World!'
    }, 200