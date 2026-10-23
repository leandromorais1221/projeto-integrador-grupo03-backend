from flask import Blueprint, jsonify
from ..models import Category
from flask_pydantic import validate
from ..schemas import CategorySchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from ..extensions import db
from uuid import UUID
from sqlalchemy import select


bp = Blueprint('categories', __name__, url_prefix='/categories')

@bp.post('')
@jwt_required()
@validate()
def categories_create(body: CategorySchema):
    """ Cria uma nova categoria de transação.

    ---
    tags:
      - Categories

    summary: Criar categoria
    description: >
      Cria uma nova categoria para o usuário autenticado.
      O identificador do usuário é obtido através do token JWT.
      A categoria pode ser do tipo receita (income) ou despesa (expense).

    security:
      - Bearer: []

    consumes:
      - application/json

    produces:
      - application/json

    parameters:
      - in: body
        name: body
        required: true
        description: Dados necessários para cadastrar a categoria.
        schema:
          type: object
          required:
            - name
            - type
          properties:
            name:
              type: string
              minLength: 3
              description: Nome da categoria, com no mínimo 3 caracteres.
              example: Alimentação

            type:
              type: string
              enum:
                - income
                - expense
              description: Tipo da categoria.
              example: expense

    responses:
      201:
        description: Categoria cadastrada com sucesso.
        examples:
          application/json:
            message: Categoria cadastrada com sucesso
            data:
              id: b1b261ab-b079-4e14-8d7c-c4a57a115119
              name: Alimentação
              type: expense
              user_id: b1b261ab-b07e-4e14-8d7c-c4a57a115119

      500:
        description: Erro interno ao cadastrar a categoria.
        examples:
          application/json:
            message: Erro consulte o suporte técnico
    """

    user_id = UUID(get_jwt_identity())

    try:
        category = Category(
            name=body.name,
            type=body.type,
            user_id=user_id
        )

        db.session.add(category)
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            'message': 'Erro consulte o suporte técnico'
        }), 500

    return jsonify({
        'message': 'Categoria cadastrada com sucesso',
        'data': category.to_dict()
    }), 201

@bp.get('')
@jwt_required()
def categories_index():
    """ Lista as categorias do usuário autenticado.

    ---
    tags:
      - Categories

    summary: Listar categorias
    description: >
      Retorna todas as categorias pertencentes ao usuário autenticado.
      O identificador do usuário é obtido através do token JWT.
      A resposta contém uma lista de categorias com seus respectivos
      identificadores, nomes e tipos.

    security:
      - Bearer: []

    produces:
      - application/json

    responses:
      200:
        description: Categorias listadas com sucesso.
        examples:
          application/json:
            data:
              - id: e20002ee-8ada-4ab9-ae82-2ad28cede321
                name: Alimentação
                type: expense
              - id: 7600d652-1be4-4974-bf5e-856f700f8103
                name: Salário
                type: income
    """
    user_id = UUID(get_jwt_identity())

    stmt = select(Category).where(Category.user_id == user_id)
    categories = db.session.execute(stmt).scalars()

    return jsonify({
        "data": [
            category.to_dict()
            for category in categories
        ]
    }), 200

@bp.put('/<uuid:category_id>')
@jwt_required()
@validate()
def categories_update(category_id: UUID, body: CategorySchema):
    """ Atualiza uma categoria existente.

    ---
    tags:
      - Categories

    summary: Atualizar categoria
    description: >
      Atualiza o nome e o tipo de uma categoria pertencente ao usuário
      autenticado. O identificador do usuário é obtido através do token JWT.
      Somente categorias pertencentes ao usuário autenticado podem ser
      atualizadas.

    security:
      - Bearer: []

    consumes:
      - application/json

    produces:
      - application/json

    parameters:
      - in: path
        name: category_id
        type: string
        format: uuid
        required: true
        description: Identificador UUID da categoria que será atualizada.
        example: 550e8400-e29b-41d4-a716-446655440000

      - in: body
        name: body
        required: true
        description: Dados atualizados da categoria.
        schema:
          type: object
          required:
            - name
            - type
          properties:
            name:
              type: string
              minLength: 3
              description: Novo nome da categoria, com no mínimo 3 caracteres.
              example: Salário

            type:
              type: string
              enum:
                - income
                - expense
              description: Novo tipo da categoria.
              example: income

    responses:
      200:
        description: Categoria atualizada com sucesso.
        examples:
          application/json:
            data:
              id: 550e8400-e29b-41d4-a716-446655440000
              name: Salário
              type: income

      404:
        description: Categoria não encontrada ou não pertencente ao usuário.
        examples:
          application/json:
            message: Categoria não encontrada

      500:
        description: Erro interno ao atualizar a categoria.
        examples:
          application/json:
            message: Erro consulte o suporte técnico
    """

    user_id = UUID(get_jwt_identity())

    stmt = select(Category).where((Category.id == category_id) & (Category.user_id == user_id))
    category = db.session.execute(stmt).scalar()

    if not category:
        return jsonify({
            'message': 'Categoria não encontrada'
        }), 404

    try:
        category.name = body.name
        category.type = body.type
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            'message': 'Erro consulte o suporte técnico'
        }), 500

    return jsonify({
        'data': category.to_dict()
    }), 200

@bp.delete('/<uuid:category_id>')
@jwt_required()
def categories_delete(category_id: UUID):
    """ Deleta uma categoria existente.

    ---
    tags:
      - Categories

    summary: Deletar categoria
    description: >
      Exclui uma categoria pertencente ao usuário autenticado.
      O identificador do usuário é obtido através do token JWT.
      Somente categorias pertencentes ao usuário autenticado podem ser
      deletadas.

    security:
      - Bearer: []

    produces:
      - application/json

    parameters:
      - in: path
        name: category_id
        type: string
        format: uuid
        required: true
        description: Identificador UUID da categoria que será deletada.
        example: 550e8400-e29b-41d4-a716-446655440000

    responses:
      200:
        description: Categoria deletada com sucesso.
        examples:
          application/json:
            message: Categoria deletada com sucesso

      404:
        description: Categoria não encontrada ou não pertencente ao usuário.
        examples:
          application/json:
            message: Categoria não encontrada

      500:
        description: Erro interno ao deletar a categoria.
        examples:
          application/json:
            message: Erro consulte o suporte técnico
    """

    user_id = UUID(get_jwt_identity())

    stmt = select(Category).where((Category.id == category_id) & (Category.user_id == user_id))
    category = db.session.execute(stmt).scalar()

    if not category:
        return jsonify({
            'message': 'Categoria não encontrada'
        }), 404

    try:
        db.session.delete(category)
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            'message': 'Erro consulte o suporte técnico'
        }), 500

    return jsonify({
        'message': 'Categoria deletada com sucesso'
    }), 200
    





