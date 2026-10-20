from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_pydantic import validate
from ..schemas import UserSchema, LoginSchema
from api_organiza_ai.extensions import db
from sqlalchemy import select
from api_organiza_ai.models import User
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.post('/register')
@validate()
def auth_register(body: UserSchema):
    """
    Cadastra um novo usuário.
    ---
    tags:
      - Usuários
    summary: Cadastro de usuário
    parameters:
      - in: body
        name: body
        required: true
        description: Dados para cadastro do usuário.
        schema:
          type: object
          required:
            - name
            - cpf
            - email
            - phone
            - password
          properties:
            name:
              type: string
              minLength: 3
              example: "João da Silva"
            cpf:
              type: string
              minLength: 11
              maxLength: 14
              example: "12345678900"
            email:
              type: string
              format: email
              example: "joao@email.com"
            phone:
              type: string
              minLength: 10
              maxLength: 15
              example: "11987654321"
            password:
              type: string
              minLength: 6
              example: "senha123"
    responses:
      400:
        description: CPF ou e-mail já cadastrado.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "CPF ou Email já cadastrado"
      500:
        description: Erro ao cadastrar o usuário.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Erro ao cadastrar o usuário."
    """

    stmt = select(User).where((User.cpf == body.cpf) | (User.email == body.email))
    registered = db.session.execute(stmt).scalar()

    if registered:
        return jsonify({
            "message": "CPF ou Email já cadastrado"
        }), 400

    try:
        user = User(
            name=body.name,
            email=body.email,
            cpf=body.cpf,
            phone=body.phone,
            password_hash=generate_password_hash(body.password)
        )

        db.session.add(user)
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "message": "Erro ao cadastrar o usuário."
        }), 500

    return jsonify({
        "data": user.to_dict()
    }), 201

@bp.post('/login')
@validate()
def auth_login(body: LoginSchema):
    """
    Autentica um usuário e retorna um token de acesso JWT.

    ---
    tags:
      - Autenticação
    summary: Realizar login
    description: >
      Autentica um usuário por meio do e-mail e da senha informados.
      Caso as credenciais sejam inválidas, retorna uma mensagem de erro.
      Em caso de sucesso, gera e retorna um token de acesso JWT.

    consumes:
      - application/json

    produces:
      - application/json

    parameters:
      - in: body
        name: body
        required: true
        description: Dados necessários para autenticação do usuário.
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              format: email
              description: E-mail cadastrado do usuário.
              example: joao@email.com
            password:
              type: string
              description: Senha do usuário.
              example: senha123

    responses:
      200:
        description: Autenticação realizada com sucesso.
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: Token JWT de acesso.
            token_type:
              type: string
              description: Tipo do token de autenticação.
              example: Bearer
        examples:
          application/json:
            access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            token_type: "Bearer"

      401:
        description: Credenciais inválidas.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Credenciais inválidas

      500:
        description: Erro interno ao consultar o banco de dados.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Erro consulte o suporte técnico.
    """
    try:
        stmt = select(User).where(User.email == body.email)
        user = db.session.execute(stmt).scalar()
    except SQLAlchemyError:
        return jsonify({
            "message": "Erro consulte o suporte técnico."
        }), 500

    if not user or not check_password_hash(
        user.password_hash,
        body.password
    ):
    
      return jsonify({
            "message": "Credenciais inválidas"
        }), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer"
    }), 200

@bp.get('/me')
@jwt_required()
def auth_me():
    """
    Retorna os dados do usuário autenticado.

    ---
    tags:
      - Autenticação
    summary: Consultar usuário autenticado
    description: >
      Obtém a identidade do usuário por meio do token JWT enviado
      na requisição e retorna seus dados cadastrais.
      Caso o usuário não seja encontrado, retorna um erro 404.
      É necessário enviar um token JWT válido para acessar este endpoint.

    produces:
      - application/json

    security:
      - Bearer: []

    responses:
      200:
        description: Dados do usuário autenticado retornados com sucesso.
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                id:
                  type: string
                  description: Identificador do usuário.
                  example: "1"
                name:
                  type: string
                  description: Nome do usuário.
                  example: "João da Silva"
                email:
                  type: string
                  format: email
                  description: E-mail do usuário.
                  example: "joao@email.com"
                cpf:
                  type: string
                  description: CPF do usuário.
                  example: "12345678900"
                phone:
                  type: string
                  description: Telefone do usuário.
                  example: "11987654321"

      401:
        description: Token JWT ausente, inválido ou expirado.
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing Authorization Header"

      404:
        description: Usuário não encontrado.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuário não encontrado"
    """
    current_user_id = UUID(get_jwt_identity())
    stmt = select(User).where(User.id == current_user_id)
    user = db.session.execute(stmt).scalar()

    if user is None:
        return jsonify({
            "message": "Usuário não encontrado"
        }), 404

    return jsonify({
        "data": user.to_dict()
    }), 200