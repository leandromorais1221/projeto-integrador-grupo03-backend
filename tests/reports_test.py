import io
import openpyxl


def test_deve_retornar_o_total_de_receitas_despesas_e_balanco_das_transacoes_do_usuario(auth):
    seed_data = {
        'income': 115297.23,
        'expense': 34149.42,
        'balance': 81147.81
    }
    response = auth.get(
        url='/reports/summary'
    )
    data = response.json
    assert response.status_code == 200
    assert data['data'] == seed_data

def test_deve_retornar_o_total_de_receitas_despesas_e_balanco_com_filtro_de_data_inicial_das_transacoes(auth):
    seed_data = {
        'income': 52432.90,
        'expense': 16501.93,
        'balance': 35930.97
    }
    response = auth.get(
        url='/reports/summary?startDate=2026-01-03'
    )
    data = response.json
    assert response.status_code == 200
    assert data['data'] == seed_data

def test_deve_retornar_o_total_de_receitas_despesas_e_balanco_com_filtro_de_data_final_das_transacoes(auth):
    seed_data = {
        'income': 62864.33,
        'expense': 17647.49,
        'balance': 45216.84
    }
    response = auth.get(
        url='/reports/summary?endDate=2025-12-18'
    )
    data = response.json
    assert response.status_code == 200
    assert data['data'] == seed_data

def test_deve_retornar_o_total_de_receitas_despesas_e_balanco_com_filtro_entre_data_final_e_inicial_das_transacoes(auth):
    seed_data = {
        'income': 57403.78,
        'expense': 22719.77,
        'balance': 34684.01
    }
    response = auth.get(
        url='/reports/summary?startDate=2025-05-02&endDate=2026-05-07'
    )
    data = response.json
    assert response.status_code == 200
    assert data['data'] == seed_data

def test_rejeita_consulta_sem_filtro_de_categoria(auth):
    response = auth.get(
        url='/reports/by-category',
    )
    validation_data = response.json['validation_error']['query_params']
    assert response.status_code == 400
    assert validation_data[0]['msg'] == 'Field required'

def test_rejeita_consulta_com_filtro_de_tipo_com_enum_invalido(auth):
    response = auth.get(
        url='/reports/by-category?type=ZyWuTPXh',
    )
    validation_data = response.json['validation_error']['query_params']
    assert response.status_code == 400
    assert validation_data[0]['msg'] == "Input should be 'income' or 'expense'"
    
def test_deve_retornar_o_total_da_categoria_e_porcentagem_com_filtro_de_tipo_ordenando_por_valor_em_ordem_descrescente(auth):
    seed_data = [
        {
            "category_id": "f7119110-d501-4434-83a5-ed75028832c3",
            "category_name": "Transporte",
            "total": 7487.48,
            "percentage": 21.93
        },
        {
            "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0",
            "category_name": "Alimentação",
            "total": 7256.44,
            "percentage": 21.25
        },
        {
            "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2",
            "category_name": "Moradia",
            "total": 7063.14,
            "percentage": 20.68
        },
        {
            "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f",
            "category_name": "Saúde",
            "total": 6980.89,
            "percentage": 20.44
        },
        {
            "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd",
            "category_name": "Lazer",
            "total": 5361.47,
            "percentage": 15.70
        }
    ]
    response = auth.get(
        url='/reports/by-category?type=expense'
    )
    data = response.json
    assert response.status_code == 200
    assert data['data'] == seed_data

def test_deve_retornar_o_total_da_categoria_e_porcentagem_com_filtro_de_tipo_e_data_inicial_ordenando_por_valor_em_ordem_descrescente(auth):
    seed_data = [
        {
            "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0",
            "category_name": "Alimentação",
            "total": 6461.04,
            "percentage": 39.15
        },
        {
            "category_id": "f7119110-d501-4434-83a5-ed75028832c3",
            "category_name": "Transporte",
            "total": 3417.84,
            "percentage": 20.71
        },
        {
            "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f",
            "category_name": "Saúde",
            "total": 3342.31,
            "percentage": 20.25
        },
        {
            "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd",
            "category_name": "Lazer",
            "total": 2256.66,
            "percentage": 13.68
        },
        {
            "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2",
            "category_name": "Moradia",
            "total": 1024.08,
            "percentage": 6.21
        }
    ]
    response = auth.get(
        url='/reports/by-category?type=expense&startDate=2026-01-03'
    )
    data = response.json
    assert response.status_code == 200
    assert data['data'] == seed_data

def test_deve_retornar_o_total_da_categoria_e_porcentagem_com_filtro_de_tipo_e_data_final_ordenando_por_valor_em_ordem_descrescente(auth):
    seed_data = [
        {
            "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2",
            "category_name": "Moradia",
            "total": 6039.06,
            "percentage": 34.22
        },
        {
            "category_id": "f7119110-d501-4434-83a5-ed75028832c3",
            "category_name": "Transporte",
            "total": 4069.64,
            "percentage": 23.06
        },
        {
            "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f",
            "category_name": "Saúde",
            "total": 3638.58,
            "percentage": 20.62
        },
        {
            "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd",
            "category_name": "Lazer",
            "total": 3104.81,
            "percentage": 17.59
        },
        {
            "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0",
            "category_name": "Alimentação",
            "total": 795.40,
            "percentage": 4.51
        }
    ]
    response = auth.get(
        url='/reports/by-category?type=expense&endDate=2025-12-18'
    )
    data = response.json
    assert response.status_code == 200
    assert data['data'] == seed_data

def test_deve_retornar_o_total_da_categoria_e_porcentagem_com_filtro_de_tipo_entre_data_final_e_inicial_ordenando_por_valor_em_ordem_descrescente(auth):
    seed_data = [
        {
            "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2",
            "category_name": "Moradia",
            "total": 6488.50,
            "percentage": 28.56
        },
        {
            "category_id": "f7119110-d501-4434-83a5-ed75028832c3",
            "category_name": "Transporte",
            "total": 6185.04,
            "percentage": 27.22
        },
        {
            "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f",
            "category_name": "Saúde",
            "total": 3976.74,
            "percentage": 17.50
        },
        {
            "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0",
            "category_name": "Alimentação",
            "total": 3054.93,
            "percentage": 13.45
        },
        {
            "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd",
            "category_name": "Lazer",
            "total": 3014.56,
            "percentage": 13.27
        }
    ]
    response = auth.get(
        url='/reports/by-category?type=expense&startDate=2025-05-02&endDate=2026-05-07'
    )
    data = response.json
    assert response.status_code == 200
    assert data['data'] == seed_data

def test_deve_retornar_o_arquivo_xlsx_com_as_transacoes(auth):
    response = auth.get(
        url='/reports/transactions-xlsx'
    )
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    assert 'relatorio.xlsx' in response.headers['Content-Disposition']
    buffer = io.BytesIO(response.data)
    spreadsheet = openpyxl.load_workbook(buffer)
    assert 'Relatório de transações' in spreadsheet.sheetnames
    tab = spreadsheet['Relatório de transações']
    assert tab['A1'].value == 'Data'
    assert tab['B1'].value == 'Descrição'
    assert tab['C1'].value == 'Categoria'
    assert tab['D1'].value == 'Tipo'
    assert tab['E1'].value == 'Valor'