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
from datetime import timedelta

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.post('/register')
@validate()
def auth_register(body: UserSchema):
    """ Cadastra um novo usuário.

    ---
    tags:
      - Autenticação
    summary: Cadastro de usuário
    description: >
      Cria uma nova conta de usuário. O CPF e o e-mail devem ser únicos.
      A senha é armazenada utilizando hash.
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: Dados necessários para cadastrar um usuário.
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
              example: "123.456.789-00"
            email:
              type: string
              format: email
              example: "joao@email.com"
            phone:
              type: string
              minLength: 10
              maxLength: 15
              example: "(11) 98765-4321"
            password:
              type: string
              minLength: 6
              format: password
              example: "123456"
    responses:
      201:
        description: Usuário cadastrado com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuário cadastrado com sucesso"
            data:
              type: object
              description: Dados do usuário cadastrado.
              properties:
                id:
                  type: string
                  example: 39272879-083d-4a12-961d-7b97a7c29b28
                name:
                  type: string
                  example: "João da Silva"
                cpf:
                  type: string
                  example: "123.456.789-00"
                email:
                  type: string
                  example: "joao@email.com"
                phone:
                  type: string
                  example: "(11) 98765-4321"
      400:
        description: CPF ou e-mail já cadastrado.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "CPF ou Email já cadastrados"
      500:
        description: Erro interno ao cadastrar o usuário.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Erro consulte o suporte técnico"
    """

    stmt = select(User).where((User.cpf == body.cpf) | (User.email == body.email))
    registered = db.session.execute(stmt).scalar()

    if registered:
        return jsonify({
            'message': 'CPF ou Email já cadastrados'
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
            'message': 'Erro consulte o suporte técnico'
        }), 500

    return jsonify({
        'message': 'Usuário cadastrado com sucesso',
        'data': user.to_dict()
    }), 201

@bp.post('/login')
@validate()
def auth_login(body: LoginSchema):
    """ Autentica um usuário e retorna um token de acesso JWT.

    ---
    tags:
      - Autenticação
    summary: Realizar login
    description: >
      Autentica um usuário por meio do e-mail e da senha informados.
      Caso as credenciais sejam inválidas, retorna uma mensagem de erro.
      Em caso de sucesso, gera um token JWT de acesso com validade de 24 horas.
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
              example: "joao@email.com"
            password:
              type: string
              format: password
              description: Senha cadastrada do usuário.
              example: "123456"
    responses:
      200:
        description: Autenticação realizada com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Login efetuado com sucesso"
            access_token:
              type: string
              description: Token JWT de acesso com validade de 24 horas.
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"
            token_type:
              type: string
              description: Tipo do token de autenticação.
              example: "Bearer"
      401:
        description: E-mail ou senha inválidos.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Email ou senha inválidos"
    """
        
    stmt = select(User).where(User.email == body.email)
    user = db.session.execute(stmt).scalar()

    if not user or not check_password_hash(user.password_hash, body.password):
      return jsonify({
          'message': 'Email ou senha inválidos'
      }), 401

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=24))

    return jsonify({
        'message': 'Login efetuado com sucesso',
        'access_token': access_token,
        'token_type': 'Bearer'
    }), 200

@bp.get('/me')
@jwt_required()
def auth_me():
    """ Retorna os dados do usuário autenticado.

    ---
    tags:
      - Autenticação
    summary: Consultar usuário autenticado
    description: >
      Obtém a identidade do usuário por meio do token JWT enviado
      na requisição e retorna seus dados cadastrais.
      É necessário enviar um token JWT válido para acessar este endpoint.
      Caso o token esteja ausente, inválido ou expirado, o acesso será negado.
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
                  example: "550e8400-e29b-41d4-a716-446655440000"
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
                  example: "123.456.789-00"
                phone:
                  type: string
                  description: Telefone do usuário.
                  example: "(11) 98765-4321"
      401:
        description: Token JWT ausente, inválido ou expirado.
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing Authorization Header"
    """
    
    current_user_id = UUID(get_jwt_identity())
    stmt = select(User).where(User.id == current_user_id)
    user = db.session.execute(stmt).scalar()
    
    return jsonify({
        'data': user.to_dict()
    }), 200


@bp.put('/me')
@jwt_required()
@validate()
def auth_update(body: UserSchema):
    """ Atualiza os dados do usuário autenticado.

    ---
    tags:
      - Autenticação
    summary: Atualizar usuário
    description: >
      Atualiza os dados pessoais do usuário autenticado, incluindo nome,
      CPF, e-mail, telefone e senha. O identificador do usuário é obtido
      através do token JWT.
      A senha deve ser armazenada utilizando hash.
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
        description: Dados necessários para atualizar o usuário.
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
              example: "123.456.789-00"
            email:
              type: string
              format: email
              example: "joao@email.com"
            phone:
              type: string
              minLength: 10
              maxLength: 15
              example: "(11) 98765-4321"
            password:
              type: string
              minLength: 6
              format: password
              example: "123456"
    responses:
      200:
        description: Usuário atualizado com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuário atualizado com sucesso"
            data:
              type: object
              description: Dados do usuário atualizado.
              properties:
                id:
                  type: string
                  example: "39272879-083d-4a12-961d-7b97a7c29b28"
                name:
                  type: string
                  example: "João da Silva"
                cpf:
                  type: string
                  example: "123.456.789-00"
                email:
                  type: string
                  example: "joao@email.com"
                phone:
                  type: string
                  example: "(11) 98765-4321"
      500:
        description: Erro interno ao atualizar os dados do usuário.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Erro consulte o suporte técnico"
    """
    current_user_id = UUID(get_jwt_identity())

    stmt = select(User).where(User.id == current_user_id)
    user = db.session.execute(stmt).scalar()

    try:
        user.name = body.name
        user.cpf = body.cpf
        user.email = body.email
        user.phone = body.phone
        user.password = generate_password_hash(body.password)
        db.session.commit()

    except SQLAlchemyError:
        return jsonify({
          'message:': 'Erro consulte o suporte técnico'
        }), 500

    return jsonify({
        'message': 'Usuário atualizado com sucesso',
        'data': user.to_dict()
    }), 200


@bp.delete('/me')
@jwt_required()
def auth_delete():
    """ Deleta a conta do usuário autenticado.

    ---
    tags:
      - Autenticação

    summary: Deletar conta
    description: >
      Exclui permanentemente a conta do usuário autenticado.
      O identificador do usuário é obtido através do token JWT.

    security:
      - Bearer: []

    produces:
      - application/json

    responses:
      200:
        description: Conta deletada com sucesso.
        examples:
          application/json:
            message: Conta deletada com sucesso

      500:
        description: Erro interno ao deletar a conta.
        examples:
          application/json:
            message: Erro consulte o suporte técnico
    """

    current_user_id = UUID(get_jwt_identity())
    stmt = select(User).where(User.id == current_user_id)
    user = db.session.execute(stmt).scalar()

    try:
      db.session.delete(user)
      db.session.commit()

    except SQLAlchemyError: 
      return jsonify({
          'message': 'Erro consulte o suporte técnico'
      }), 500

    return jsonify({
       'message': 'Conta deletada com sucesso'
    }), 200
        
    