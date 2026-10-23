from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from flask_pydantic import validate
from ..schemas import TransactionSchema
from ..models import Transaction, Category
from ..extensions import db


bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.post('')
@jwt_required()
@validate()
def transactions_create(body: TransactionSchema):
    """ Cadastra uma nova transação.

    ---
    tags:
      - Transactions

    summary: Criar transação
    description: >
      Cadastra uma nova transação para o usuário autenticado.
      A transação deve estar vinculada a uma categoria existente
      pertencente ao mesmo usuário. O identificador do usuário
      é obtido através do token JWT.

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
        description: Dados necessários para cadastrar a transação.
        schema:
          type: object
          required:
            - description
            - amount
            - type
            - date
            - payment_method
            - category_id
          properties:
            description:
              type: string
              minLength: 3
              description: Descrição da transação, com no mínimo 3 caracteres.
              example: Compra no supermercado

            amount:
              type: number
              format: decimal
              minimum: 0
              exclusiveMinimum: true
              description: Valor da transação, maior que zero.
              example: 150.75

            type:
              type: string
              enum:
                - income
                - expense
              description: Tipo da transação.
              example: expense

            date:
              type: string
              format: date
              description: Data da transação no formato YYYY-MM-DD.
              example: "2026-10-20"

            payment_method:
              type: string
              enum:
                - credito
                - debito
                - pix
                - dinheiro
                - boleto
              description: Método de pagamento utilizado.
              example: pix

            category_id:
              type: string
              format: uuid
              description: Identificador UUID da categoria.
              example: 550e8400-e29b-41d4-a716-446655440000

    responses:
      201:
        description: Transação cadastrada com sucesso.
        examples:
          application/json:
            message: Transação cadastrada com sucesso
            data:
              id: 550e8400-e29b-41d4-a716-446655440001
              description: Compra no supermercado
              amount: 150.75
              type: expense
              date: "2026-10-20"
              payment_method: pix
              category_id: 550e8400-e29b-41d4-a716-446655440000

      404:
        description: Categoria não encontrada ou não pertencente ao usuário.
        examples:
          application/json:
            message: Categoria não encontrada

      500:
        description: Erro interno ao cadastrar a transação.
        examples:
          application/json:
            message: Erro consulte o suporte técnico
    """
    
    user_id = UUID(get_jwt_identity())

    stmt = select(Category).where((Category.user_id == user_id) & (Category.id == body.category_id))
    category_exists = db.session.execute(stmt).scalar()

    if not category_exists:
        return jsonify({
            'message': 'Categoria não encontrada'
        }), 404

    try:
        transaction = Transaction(
            description=body.description,
            amount=body.amount,
            type=body.type,
            date=body.date,
            payment_method=body.payment_method,
            user_id=user_id,
            category_id=body.category_id
        )

        db.session.add(transaction)
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            'message': 'Erro consulte o suporte técnico'
        }), 500

    return jsonify({
        'message': 'Transação cadastrada com sucesso',
        'data': transaction.to_dict()
    }), 201

@bp.get('')
@jwt_required()
def transactions_index():
    """ Lista as transações do usuário autenticado.

    ---
    tags:
      - Transactions

    summary: Listar transações
    description: >
      Retorna todas as transações pertencentes ao usuário autenticado.
      O identificador do usuário é obtido através do token JWT.

    security:
      - Bearer: []

    produces:
      - application/json

    responses:
      200:
        description: Transações listadas com sucesso.
        examples:
          application/json:
            data:
              - id: 550e8400-e29b-41d4-a716-446655440001
                description: Compra no supermercado
                amount: 150.75
                type: expense
                date: "2026-10-20"
                payment_method: pix
                user_id: 550e8400-e29b-41d4-a716-446655440002
                category_id: 550e8400-e29b-41d4-a716-446655440000
              - id: 550e8400-e29b-41d4-a716-446655440003
                description: Salário
                amount: 2500.00
                type: income
                date: "2026-10-05"
                payment_method: credito
                user_id: 550e8400-e29b-41d4-a716-446655440002
                category_id: 550e8400-e29b-41d4-a716-446655440004
    """
    
    user_id = UUID(get_jwt_identity())

    stmt = select(Transaction).where(Transaction.user_id == user_id)
    transactions = db.session.execute(stmt).scalars()

    return jsonify({
        'data': [ transaction.to_dict() for transaction in transactions ]
    }), 200

@bp.put('/<uuid:transaction_id>')
@jwt_required()
@validate()
def transactions_update(transaction_id: UUID, body: TransactionSchema):
    """ Atualiza uma transação existente.

    ---
    tags:
      - Transactions

    summary: Atualizar transação
    description: >
      Atualiza os dados de uma transação pertencente ao usuário autenticado.
      A categoria informada deve existir e pertencer ao mesmo usuário.
      O identificador do usuário é obtido através do token JWT.

    security:
      - Bearer: []

    consumes:
      - application/json

    produces:
      - application/json

    parameters:
      - in: path
        name: transaction_id
        type: string
        format: uuid
        required: true
        description: Identificador UUID da transação que será atualizada.
        example: 550e8400-e29b-41d4-a716-446655440001

      - in: body
        name: body
        required: true
        description: Dados atualizados da transação.
        schema:
          type: object
          required:
            - description
            - amount
            - type
            - date
            - payment_method
            - category_id
          properties:
            description:
              type: string
              minLength: 3
              description: Descrição da transação, com no mínimo 3 caracteres.
              example: Compra no supermercado

            amount:
              type: number
              format: decimal
              minimum: 0
              exclusiveMinimum: true
              description: Valor da transação, maior que zero.
              example: 150.75

            type:
              type: string
              enum:
                - income
                - expense
              description: Tipo da transação.
              example: expense

            date:
              type: string
              format: date
              description: Data da transação no formato YYYY-MM-DD.
              example: "2026-10-20"

            payment_method:
              type: string
              enum:
                - credito
                - debito
                - pix
                - dinheiro
                - boleto
              description: Método de pagamento utilizado.
              example: pix

            category_id:
              type: string
              format: uuid
              description: Identificador UUID da categoria.
              example: 550e8400-e29b-41d4-a716-446655440000

    responses:
      200:
        description: Transação atualizada com sucesso.
        examples:
          application/json:
            message: Transação atualizada com sucesso
            data:
              id: 550e8400-e29b-41d4-a716-446655440001
              description: Compra no supermercado
              amount: 150.75
              type: expense
              date: "2026-10-20"
              payment_method: pix
              category_id: 550e8400-e29b-41d4-a716-446655440000

      404:
        description: Transação ou categoria não encontrada ou não pertencente ao usuário.
        examples:
          application/json:
            message: Transação não encontrada

      500:
        description: Erro interno ao atualizar a transação.
        examples:
          application/json:
            message: Erro consulte o suporte técnico
    """
    
    user_id = UUID(get_jwt_identity())

    category_stmt = select(Category).where((Category.user_id == user_id) & (Category.id == body.category_id))
    category_exists = db.session.execute(category_stmt).scalar()

    if not category_exists:
        return jsonify({
            'message': 'Categoria não encontrada'
        }), 404

    transaction_stmt = select(Transaction).where((Transaction.user_id == user_id) & (Transaction.id == transaction_id))
    transaction_exists = db.session.execute(transaction_stmt).scalar()

    if not transaction_exists:
        return jsonify({
            'message': 'Transação não encontrada'
        }), 404

    try:
        transaction_exists.description = body.description
        transaction_exists.amount = body.amount
        transaction_exists.type = body.type
        transaction_exists.date = body.date
        transaction_exists.payment_method = body.payment_method
        transaction_exists.category_id = body.category_id

        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            'message': 'Erro consulte o suporte técnico'
        }), 500

    return jsonify({
        'message': 'Transação atualizada com sucesso',
        'data': transaction_exists.to_dict()
    }), 200

@bp.delete('/<uuid:transaction_id>')
@jwt_required()
def transactions_delete(transaction_id: UUID):
    """ Deleta uma transação existente.

    ---
    tags:
      - Transactions

    summary: Deletar transação
    description: >
      Exclui uma transação pertencente ao usuário autenticado.
      O identificador do usuário é obtido através do token JWT.
      Somente transações pertencentes ao usuário autenticado podem ser
      deletadas.

    security:
      - Bearer: []

    produces:
      - application/json

    parameters:
      - in: path
        name: transaction_id
        type: string
        format: uuid
        required: true
        description: Identificador UUID da transação que será deletada.
        example: 550e8400-e29b-41d4-a716-446655440001

    responses:
      200:
        description: Transação deletada com sucesso.
        examples:
          application/json:
            message: Transação deletada com sucesso

      404:
        description: Transação não encontrada ou não pertencente ao usuário.
        examples:
          application/json:
            message: Transação não encontrada

      500:
        description: Erro interno ao deletar a transação.
        examples:
          application/json:
            message: Erro consulte o suporte técnico
    """
        
    user_id = UUID(get_jwt_identity())

    stmt = select(Transaction).where((Transaction.user_id == user_id) & (Transaction.id == transaction_id))
    transaction = db.session.execute(stmt).scalar()

    if not transaction:
        return jsonify({
            'message': 'Transação não encontrada'
        }), 404

    try:
        db.session.delete(transaction)
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            'message': 'Erro consulte o suporte técnico'
        }), 500

    return jsonify({
        'message': 'Transação deletada com sucesso'
    }), 200

    
