from api_organiza_ai.config.extensions import db
from api_organiza_ai.models import User
from sqlalchemy import select

def test_rejeita_nome_com_menos_de_3_caracteres(client):
    body = {
        'name': 'Us'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    assert response.status_code == 400
    validation_data = response.json['validation_error']['body_params'][0]
    assert validation_data['msg'] == 'String should have at least 3 characters'

def test_rejeita_nome_com_mais_de_120_caracteres(client):
    body = {
        'name': 'NOGlvBeKjhJovhZ5VEj71Kmtx3urPMzglPrzXe6Uj0iSLE7L3799dV79ocWBp1l40nQ6jVM4xuWsDYHSXhCA2bey8p3mr5uGRYoEOFh7RhMMomxp3pLMlumFaoML660J'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    assert response.status_code == 400
    validation_data = response.json['validation_error']['body_params'][0]
    assert validation_data['msg'] == 'String should have at most 120 characters'

def test_rejeita_cpf_com_menos_de_11_caracteres(client):
    body = {
        'cpf': '9467246740'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    assert response.status_code == 400
    validation_data = response.json['validation_error']['body_params'][1]
    assert validation_data['msg'] == 'String should have at least 11 characters'

def test_rejeita_cpf_com_mais_de_14_caractres(client):
    body = {
        'cpf': '946.724.674-000'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    assert response.status_code == 400
    validation_data = response.json['validation_error']['body_params'][1]
    assert validation_data['msg'] == 'String should have at most 14 characters'

def test_rejeita_email_invalido(client):
    body = {
        'email': 'usuarioteste.com'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    assert response.status_code == 400
    validation_data = response.json['validation_error']['body_params'][2]
    assert validation_data['msg'] == 'value is not a valid email address: An email address must have an @-sign.'

def test_rejeita_telefone_com_menos_de_10_caracteres(client):
    body = {
        'phone': '119845219'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    assert response.status_code == 400
    validation_data = response.json['validation_error']['body_params'][3]
    assert validation_data['msg'] == 'String should have at least 10 characters'

def test_rejeita_telefone_com_mais_de_15_caracteres(client):
    body = {
        'phone': '(11) 98452-19871'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    assert response.status_code == 400
    validation_data = response.json['validation_error']['body_params'][3]
    assert validation_data['msg'] == 'String should have at most 15 characters'

def test_rejeita_senha_com_menos_de_6_caracteres(client):
    body = {
        'password': '03094'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    assert response.status_code == 400
    validation_data = response.json['validation_error']['body_params'][4]
    assert validation_data['msg'] == 'String should have at least 6 characters'

def test_registra_usuario_com_dados_validos(client, app):
    body = {
        'name': 'Usuario Teste',
        'cpf': '009.334.541-82',
        'email': 'usuarioteste@gmail.com',
        'phone': '(11) 98452-1987',
        'password': 'teste123456'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    data = response.json
    with app.app_context():
        stmt = select(User).where(
            User.email == data['data']['email']
        )
        user = db.session.execute(stmt).scalar()
    assert user is not None
    assert response.status_code == 201
    assert data['message'] == 'Usuário cadastrado com sucesso'
    assert 'id' in response.json['data']
    assert data['data']['name'] == body['name']
    assert data['data']['cpf'] == body['cpf']
    assert data['data']['email'] == body['email']
    assert data['data']['phone'] == body['phone']
    assert 'password' not in data['data']

def test_rejeita_cadastro_de_cpf_e_email_ja_cadastrado(client, app):
    body = {
        'name': 'Usuario Teste Duplicado',
        'cpf': '009.339.541-82',
        'email': 'usuarioteste@gmail.com',
        'phone': '(11) 98452-1987',
        'password': 'teste123456'
    }
    with app.app_context():
        stmt = select(User).where(
            User.email == body['email']
        )
        user_exists = db.session.execute(stmt).scalar()
        if not user_exists:
            client.post('/auth/register', json=body)
    response = client.post('/auth/register', json=body)
    assert response.status_code == 409
    data = response.json
    

    assert data['message'] == 'CPF ou Email já cadastrados'


def test_rejeita_login_sem_email_e_senha(client):
    response = client.post(
        '/auth/login',
        json={}
    )
    data = response.json
    validation_data = response.json['validation_error']['body_params']
    assert response.status_code == 400
    assert 'access_token' not in data
    assert 'token_type' not in data
    assert validation_data[0]['msg'] == "Field required"
    assert validation_data[1]['msg'] == "Field required"

def test_valida_se_login_retorna_access_token(client):
    body = {
        'email': 'usuarioteste@gmail.com',
        'password': 'teste123456'
    }
    response = client.post(
        '/auth/login',
        json=body
    )
    data = response.json
    assert response.status_code == 200
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['message'] == 'Login efetuado com sucesso'

def test_rejeita_login_com_credenciais_inválidas(client):
    body = {
        'email': 'usuarioteste@gmail.com',
        'password': 'teste'
    }
    response = client.post(
        '/auth/login',
        json=body
    )
    data = response.json
    assert response.status_code == 401
    assert 'access_token' not in data
    assert 'token_type' not in data
    assert data['message'] == 'Email ou senha inválidos'

def test_rota_get_me_rejeita_token_asuente(client):
    response = client.get(
        '/auth/me'
    )
    data = response.json
    assert response.status_code == 401
    assert 'access_token' not in data
    assert 'token_type' not in data
    assert data['msg'] == 'Missing Authorization Header'

def test_rota_put_me_rejeita_token_asuente(client):
    response = client.put(
        '/auth/me'
    )
    data = response.json
    assert response.status_code == 401
    assert 'access_token' not in data
    assert 'token_type' not in data
    assert data['msg'] == 'Missing Authorization Header'

def test_rota_delete_me_rejeita_token_asuente(client):
    response = client.delete(
        '/auth/me'
    )
    data = response.json
    assert response.status_code == 401
    assert 'access_token' not in data
    assert 'token_type' not in data
    assert data['msg'] == 'Missing Authorization Header'

def test_rota_me_deve_retornar_informacoes_do_usuario_logado(auth):
    response = auth.get(
        url='/auth/me'
    )
    user = auth.get_user()
    data = response.json['data']
    assert response.status_code == 200
    assert data['id'] == str(user.id)
    assert data['name'] == user.name
    assert data['email'] == user.email
    assert data['cpf'] == user.cpf
    assert data['phone'] == user.phone

def test_rota_me_deve_atualizar_informacoes_do_usuario_logado(auth, app):
    body = {
        'name': 'Usuario',
        'cpf': '009.334.541-82',
        'email': 'usuario@gmail.com',
        'phone': '(11) 98452-1987',
        'password': 'teste123456'
    }
    response = auth.put(
        url='/auth/me', 
        body=body
    )

    with app.app_context():
        stmt = select(User).where(
            User.email == body['email'],
            User.cpf == body['cpf']
        )
        user = db.session.execute(stmt).scalar()

    data = response.json
    assert response.status_code == 200
    assert user.name == body['name']
    assert user.email == body['email']
    assert user.cpf == body['cpf']
    assert user.phone == body['phone']
    assert data['message'] == 'Usuário atualizado com sucesso'

def test_rota_me_deve_excluir_conta_do_usuario_logado(auth, app):

    user_logged = auth.get_user()

    response = auth.delete(
        url='/auth/me'
    )

    with app.app_context():
        stmt = select(User).where(
            User.id == user_logged.id,
        )
        user = db.session.execute(stmt).scalar()

    data = response.json
    assert user is None
    assert response.status_code == 200
    assert data['message'] == 'Conta deletada com sucesso'
