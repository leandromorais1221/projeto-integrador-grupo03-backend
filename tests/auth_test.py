

def test_rejeita_nome_com_menos_de_3_caracteres(client):
    body = {
        'name': 'Us'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    validation_data = response.json['validation_error']['body_params'][0]
    assert response.status_code == 400
    assert validation_data['msg'] == 'String should have at least 3 characters'

def test_rejeita_cpf_com_menos_de_11_caracteres(client):
    body = {
        'cpf': '9467246740'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    validation_data = response.json['validation_error']['body_params'][1]
    assert response.status_code == 400
    assert validation_data['msg'] == 'String should have at least 11 characters'

def test_rejeita_cpf_com_mais_de_14_caractres(client):
    body = {
        'cpf': '946.724.674-000'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    validation_data = response.json['validation_error']['body_params'][1]
    assert response.status_code == 400
    assert validation_data['msg'] == 'String should have at most 14 characters'

def test_rejeita_email_invalido(client):
    body = {
        'email': 'usuarioteste.com'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    validation_data = response.json['validation_error']['body_params'][2]
    assert response.status_code == 400
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

def test_registra_usuario_com_dados_validos(client):
    body = {
        'name': 'Usuario Teste',
        'cpf': '009.339.541-82',
        'email': 'usuarioteste@gmail.com',
        'phone': '(11) 98452-1987',
        'password': 'teste123456'
    }
    response = client.post(
        '/auth/register',
        json=body
    )
    data = response.json
    assert response.status_code == 201
    assert data['message'] == 'Usuário cadastrado com sucesso.'
    assert 'id' in response.json['data']
    assert data['data']['name'] == body['name']
    assert data['data']['cpf'] == body['cpf']
    assert data['data']['email'] == body['email']
    assert data['data']['phone'] == body['phone']
    assert 'password' not in data['data']

def test_rejeita_cadastro_de_cpf_e_email_ja_cadastrado(client):
    body = {
        'name': 'Usuario Teste',
        'cpf': '009.339.541-82',
        'email': 'usuarioteste@gmail.com',
        'phone': '(11) 98452-1987',
        'password': 'teste123456'
    }
    reponse = client.post(
        '/auth/register',
        json=body
    )
    data = reponse.json
    assert reponse.status_code == 400
    assert data['message'] == "CPF ou Email já cadastrado"


def test_rejeita_login_sem_email_e_senha(client):
    response = client.post(
        '/auth/login',
        json={}
    )
    assert response.status_code == 400
    validation_data = response.json['validation_error']['body_params'][0]
    assert validation_data['msg'] == "Field required"
    validation_data = response.json['validation_error']['body_params'][1]
    assert validation_data['msg'] == "Field required"


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
    assert data['message'] == 'Login efetuado com sucesso.'

def test_deve_retornar_informacoes_do_usuario_logado(auth):
    response = auth.get(
        url='/auth/me'
    )
    data = response.json['data']
    assert response.status_code == 200
    assert 'id' in data
    assert 'cpf' in data
    assert 'email' in data
    assert 'name' in data
    assert 'phone' in data

