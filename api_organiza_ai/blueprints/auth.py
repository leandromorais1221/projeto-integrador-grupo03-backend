from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api_organiza_ai.extensions import db
from api_organiza_ai.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

#registro
@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json() or {}

  name = data.get('name', '').strip()
  cpf = data.get('cpf', '')
  email = data.get('email', '')
  password = data.get('password', '')

  raw_phone = data.get('phone', '')
  phone = ''.join(filter(str.isdigit, raw_phone))

  #Validação
  if len(name) < 3:
    return jsonify({"message": "O nome deve ter no mínimo 3 caracteres."}), 400
  if not cpf or len(cpf) < 11:
        return jsonify({"message": "CPF inválido."}), 400
  if not email or '@' not in email:
        return jsonify({"message": "E-mail inválido."}), 400
  if not phone or len(phone) not in [10, 11]:
        return jsonify({"message": "Telefone inválido."}), 400
  if not password or len(password) < 6:
        return jsonify({"message": "A senha deve ter no mínimo 6 caracteres."}), 400


  if db.session.scalar(db.select(User).where(User.cpf == cpf)):
        return jsonify({"message": "CPF já cadastrado"}), 400
  if db.session.scalar(db.select(User).where(User.email == email)):
        return jsonify({"message": "E-mail já cadastrado"}), 400

  #utilizador
  new_user = User(
        name=name,
        email=email,
        cpf=cpf,
        phone=phone, 
        password_hash=generate_password_hash(password)
    )

  try:
      db.session.add(new_user)
      db.session.commit()
  except Exception as e:
      db.session.rollback()
      return jsonify({"message": "Erro interno ao cadastrar o usuário."}), 500

  #resposta
  return jsonify({
        "id": str(new_user.id),
        "name": new_user.name,
        "email": new_user.email,
        "cpf": new_user.cpf,
        "phone": new_user.phone
    }), 201

#login
@auth_bp.route('/login', methods = ['POST'])
def login():
     data = request.get_json() or {}

     email = data.get('email')
     password = data.get('password')

     try:
       user = db.session.scalar(db.select(User).where(User.email == email))
     except Exception as e:
       return jsonify({"message": "Erro interno ao consultar o banco de dados."}), 500

     if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Credenciais inválidas"}), 401

     access_token = create_access_token(identity=str(user.id))

     #resposta
     return jsonify({
        "access_token": access_token,
        "token_type": "Bearer"
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
  current_user_id = get_jwt_identity()
  user = db.session.scalar(db.select(User).where(User.id == current_user_id))

  if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

  return jsonify({
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "cpf": user.cpf,
        "phone": user.phone
    }), 200