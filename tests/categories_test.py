from api.config.extensions import db
from api.models import Category
from sqlalchemy import select
from uuid import UUID


def test_rejeita_nome_com_menos_de_3_caracteres(auth):
    body = {
        'name': ''
    }
    response = auth.post(
        url='/categories',
        body=body
    )
    validation_data = response.json['validation_error']['body_params']
    assert response.status_code == 400
    assert validation_data[0]['msg'] == 'String should have at least 3 characters'

def test_rejeita_nome_com_mais_de_50_caracteres(auth):
    body = {
        'name': 'LTUDZ3YcUNdjU0XgevKcBhcEjKqi6OiI1L8YtpiQq1aUN8j8wel4eftbxAucD3zo'
    }
    response = auth.post(
        url='/categories',
        body=body
    )
    validation_data = response.json['validation_error']['body_params']
    assert response.status_code == 400
    assert validation_data[0]['msg'] == 'String should have at most 50 characters'

def test_rejeita_enum_de_tipo_inválido(auth):
    body = {
        'type': 'XbWvC15O'
    }
    response = auth.post(
        url='/categories',
        body=body
    )
    validation_data = response.json['validation_error']['body_params']
    assert response.status_code == 400
    assert validation_data[1]['msg'] == "Input should be 'income' or 'expense'"

def test_registra_categoria_com_dados_validos(auth, app):
    body = {
        'name': 'Aluguel',
        'type': 'income'
    }
    response = auth.post(
        url='/categories',
        body=body
    )
    with app.app_context():
        stmt = select(Category).where(
            Category.name == body['name'],
            Category.type == body['type']
        )
        category = db.session.execute(stmt).scalar()

    data = response.json
    assert category is not None
    assert response.status_code == 201
    assert data['data']['name'] == body['name']
    assert data['data']['type'] == body['type']
    assert data['message'] == 'Categoria cadastrada com sucesso'

def test_rejeita_cadastro_de_categoria_e_tipo_ja_cadastrados(auth, app):
    body = {
        'name': 'Salário',
        'type': 'income'
    }
    response = auth.post(
        url='/categories',
        body=body
    )
    data = response.json
    assert response.status_code == 409
    assert data['message'] == 'Categoria já cadastrada'

def test_deve_retornar_as_categorias_do_usuario(auth):
    seed_data = [
        {
            "id": "8cd39aba-d319-4869-96f0-915ae03cecb0",
            "name": "Alimentação",
            "type": "expense"
        },
        {
            "id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2",
            "name": "Moradia",
            "type": "expense"
        },
        {
            "id": "f7119110-d501-4434-83a5-ed75028832c3",
            "name": "Transporte",
            "type": "expense"
        },
        {
            "id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd",
            "name": "Lazer",
            "type": "expense"
        },
        {
            "id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f",
            "name": "Saúde",
            "type": "expense"
        },
        {
            "id": "d924100a-d337-46c2-ad60-78b18a124568",
            "name": "Salário",
            "type": "income"
        },
        {
            "id": "b73c62d9-e2ac-4fad-b5f8-f6a58e2fc9a7",
            "name": "Freelance",
            "type": "income"
        },
        {
            "id": "8605b267-eb24-4810-bb60-6d5212b4f50e",
            "name": "Investimentos",
            "type": "income"
        },
        {
            "id": "8e3de990-a7e0-4935-8b90-0afc65e3241a",
            "name": "Vendas",
            "type": "income"
        },
        {
            "id": "2870cacd-8fe8-4433-82c4-2b09e410153d",
            "name": "Outras Receitas",
            "type": "income"
        }
    ]

    request = auth.get(
        url='/categories'
    )
    data = request.json
    assert request.status_code == 200
    assert data['data'] == seed_data

def test_atualiza_categoria_existente_do_usuario(auth, app):
    with app.app_context():
        category = Category(
            name='Aluguel',
            type='income',
            user_id=UUID('fa8a6508-a7e6-4bad-8125-e0fcc369f9e1')
        )
        db.session.add(category)
        db.session.commit()

        category_id = category.id
    body = {
        'name': 'Aluguel Atualizado',
        'type': 'income',
    }
    request = auth.put(
        url=f'/categories/{category_id}',
        body=body
    )
    data = request.json
    assert request.status_code == 200
    assert data['data']['name'] == body['name']
    assert data['data']['type'] == body['type']
    assert data['message'] == 'Categoria atualizada com sucesso'

def test_rejeita_atualizar_categoria_nao_cadastrada(auth, app):
    category_id = '2ac30dfa-5665-4112-a61b-3ffbcd99f808'
    body = {
        'name': 'Academia Atualizada',
        'type': 'expense',
    }
    request = auth.put(
        url=f'/categories/{category_id}',
        body=body
    )
    with app.app_context():
        stmt = select(Category).where(
            Category.id == UUID(category_id)
        )
        category = db.session.execute(stmt).scalar()
        assert category is None
    data = request.json
    assert request.status_code == 404
    assert data['message'] == 'Categoria não encontrada'


def test_rejeita_atualizar_categoria_com_transacoes_vinculadas(auth, app):
    category_id = 'd924100a-d337-46c2-ad60-78b18a124568'
    body = {
        'name': 'Salário Atualizado',
        'type': 'income',
    }
    request = auth.put(
        url=f'/categories/{category_id}',
        body=body
    )
    with app.app_context():
        stmt = select(Category).where(
            Category.id == UUID(category_id)
        )
        category = db.session.execute(stmt).scalar()
        assert category.transactions is not None
    data = request.json
    assert request.status_code == 409
    assert data['message'] == 'Erro a categoria não pode ser atualizada pois há transações vinculadas'

def test_deleta_categoria_existente(auth, app):
    with app.app_context():
        category = Category(
            name='Aluguel',
            type='income',
            user_id=UUID('fa8a6508-a7e6-4bad-8125-e0fcc369f9e1')
        )
        db.session.add(category)
        db.session.commit()
        category_id = category.id
    request = auth.delete(
        url=f'/categories/{category_id}'
    )
    data = request.json
    assert request.status_code == 200
    assert data['message'] == 'Categoria deletada com sucesso'

def test_rejeita_deletar_categoria_nao_cadastrada(auth, app):
    category_id = '2ac30dfa-5665-4112-a61b-3ffbcd99f808'
    request = auth.delete(
        url=f'/categories/{category_id}'
    )
    with app.app_context():
        stmt = select(Category).where(
            Category.id == UUID(category_id)
        )
        category = db.session.execute(stmt).scalar()
        assert category is None
    data = request.json
    assert request.status_code == 404
    assert data['message'] == 'Categoria não encontrada'

def test_rejeita_deletar_categoria_com_transacoes_vinculadas(auth, app):
    category_id = 'd924100a-d337-46c2-ad60-78b18a124568'
    request = auth.delete(
        url=f'/categories/{category_id}'
    )
    with app.app_context():
        stmt = select(Category).where(
            Category.id == UUID(category_id)
        )
        category = db.session.execute(stmt).scalar()
        assert category.transactions is not None
    data = request.json
    assert request.status_code == 409
    assert data['message'] == 'Erro a categoria não pode ser excluída pois há transações vinculadas'