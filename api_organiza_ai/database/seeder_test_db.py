from ..models import User, Category, Transaction
from uuid import UUID
from ..config.extensions import db
from datetime import datetime

def mock_db():
    user = {
        "id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "name": "Usuario Teste",
        "email": "usuario.teste@email.com",
        "cpf": "009.339.541-82",
        "phone": "(11) 3456-7890",
        "password_hash": "scrypt:32768:8:1$5jEuzK92hXqSA2bd$22aa5c999925f43036a8176542706f7ff16b41d6e84669d4552dd3c5aad34a8a3eb970344a9ed48d85d9f22bf55ed827b7f57fdc9c9831a5fb40d837df2a5f9b",
    }

    categories = [
        {
            "id": "8cd39aba-d319-4869-96f0-915ae03cecb0",
            "name": "Alimentação",
            "type": "expense",
            "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1"
        },
        {
            "id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2",
            "name": "Moradia",
            "type": "expense",
            "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1"
        },
        {
            "id": "f7119110-d501-4434-83a5-ed75028832c3",
            "name": "Transporte",
            "type": "expense",
            "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1"
        },
        {
            "id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd",
            "name": "Lazer",
            "type": "expense",
            "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1"
        },
        {
            "id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f",
            "name": "Saúde",
            "type": "expense",
            "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1"
        },
        {
            "id": "d924100a-d337-46c2-ad60-78b18a124568",
            "name": "Salário",
            "type": "income",
            "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1"
        },
        {
            "id": "b73c62d9-e2ac-4fad-b5f8-f6a58e2fc9a7",
            "name": "Freelance",
            "type": "income",
            "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1"
        },
        {
            "id": "8605b267-eb24-4810-bb60-6d5212b4f50e",
            "name": "Investimentos",
            "type": "income",
            "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1"
        },
        {
            "id": "8e3de990-a7e0-4935-8b90-0afc65e3241a",
            "name": "Vendas",
            "type": "income",
            "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1"
        },
        {
            "id": "2870cacd-8fe8-4433-82c4-2b09e410153d",
            "name": "Outras Receitas",
            "type": "income",
            "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1"
        }
    ]

    transactions = [
    {
        "id": "539f9e62-074e-4084-ba06-7314b2a83740",
        "description": "Pizzaria Bella Italia",
        "amount": 52.14,
        "type": "expense",
        "date": "2026-04-08",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0"
    },
    {
        "id": "da1a5cec-1045-4c32-9ba8-d114643a879a",
        "description": "Gás Encanado - Comgás",
        "amount": 167.21,
        "type": "expense",
        "date": "2025-10-14",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2"
    },
    {
        "id": "b85ce0d3-80d6-4bdd-ab50-22cd85b528b6",
        "description": "Posto Ipiranga - Gasolina",
        "amount": 154.14,
        "type": "expense",
        "date": "2025-09-20",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "f7119110-d501-4434-83a5-ed75028832c3"
    },
    {
        "id": "d50eff5a-4640-4df8-bd5e-30e36f73f7ee",
        "description": "Livro - Livraria Cultura",
        "amount": 1078.29,
        "type": "expense",
        "date": "2026-04-15",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd"
    },
    {
        "id": "a5469e28-ac9c-418f-adc3-d9c5642bed4b",
        "description": "Farmácia Droga Raia",
        "amount": 1217.0,
        "type": "expense",
        "date": "2025-03-23",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f"
    },
    {
        "id": "039a0daa-5650-4b4a-8ebd-e143b51ee201",
        "description": "13º Salário Parcela",
        "amount": 1403.8,
        "type": "income",
        "date": "2025-06-04",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "d924100a-d337-46c2-ad60-78b18a124568"
    },
    {
        "id": "042e3bd6-4169-4b97-919c-ee3df4842400",
        "description": "Manutenção de Sistema - Freelance",
        "amount": 501.65,
        "type": "income",
        "date": "2026-10-09",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "b73c62d9-e2ac-4fad-b5f8-f6a58e2fc9a7"
    },
    {
        "id": "d9bd066e-c070-4047-883d-0fbe53039a99",
        "description": "Rendimento Poupança",
        "amount": 2690.42,
        "type": "income",
        "date": "2026-02-18",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8605b267-eb24-4810-bb60-6d5212b4f50e"
    },
    {
        "id": "e5612e31-0230-46e8-b34b-88d6e242bd4a",
        "description": "Venda de Peças / Acessórios",
        "amount": 2895.21,
        "type": "income",
        "date": "2025-01-22",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8e3de990-a7e0-4935-8b90-0afc65e3241a"
    },
    {
        "id": "48a8babe-bbcc-4a32-813a-1c5bd4dbbe40",
        "description": "Venda Pontos / Milhas",
        "amount": 4926.4,
        "type": "income",
        "date": "2025-02-13",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2870cacd-8fe8-4433-82c4-2b09e410153d"
    },
    {
        "id": "e4b93ef0-0aa1-48e6-844a-489b22e23f95",
        "description": "Supermercado Pão de Açúcar",
        "amount": 958.99,
        "type": "expense",
        "date": "2026-03-12",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0"
    },
    {
        "id": "42629426-9238-4903-b0be-3c10ff0399fa",
        "description": "Conta de Luz - Enel/CPFL",
        "amount": 1010.21,
        "type": "expense",
        "date": "2025-10-21",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2"
    },
    {
        "id": "eb8247f4-3eb7-4c1b-ba5e-ce55063f0f33",
        "description": "Pedágio AutoBann/ViaOeste",
        "amount": 1097.75,
        "type": "expense",
        "date": "2025-08-13",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "f7119110-d501-4434-83a5-ed75028832c3"
    },
    {
        "id": "2985914d-0eb7-453c-bd7b-8a17bd970cd9",
        "description": "Livro - Livraria Cultura",
        "amount": 1031.65,
        "type": "expense",
        "date": "2025-04-27",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd"
    },
    {
        "id": "00e8929b-3984-4c1b-a6d9-8de5012a0325",
        "description": "Suplementos Alimentares",
        "amount": 483.45,
        "type": "expense",
        "date": "2026-02-07",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f"
    },
    {
        "id": "88b3ac65-6bb2-4765-a733-32bf8cbb54aa",
        "description": "13º Salário Parcela",
        "amount": 1078.88,
        "type": "income",
        "date": "2026-07-21",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "d924100a-d337-46c2-ad60-78b18a124568"
    },
    {
        "id": "45814a9b-5af5-442c-b95e-39e8f5f4e7af",
        "description": "Consultoria de TI",
        "amount": 1339.1,
        "type": "income",
        "date": "2025-12-18",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "b73c62d9-e2ac-4fad-b5f8-f6a58e2fc9a7"
    },
    {
        "id": "7438fb6e-fdfb-45fa-b9ec-1785a409942a",
        "description": "Resgate Parcial Investimentos",
        "amount": 3740.13,
        "type": "income",
        "date": "2026-10-13",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8605b267-eb24-4810-bb60-6d5212b4f50e"
    },
    {
        "id": "bc900987-6f21-4ee0-a8ef-5f13355300c9",
        "description": "Venda de Equipamento Antigo",
        "amount": 4986.68,
        "type": "income",
        "date": "2025-09-16",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8e3de990-a7e0-4935-8b90-0afc65e3241a"
    },
    {
        "id": "006ede31-d5cd-407b-8784-a26ba676eab0",
        "description": "Transferência Recebida - PIX",
        "amount": 4308.29,
        "type": "income",
        "date": "2025-11-06",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2870cacd-8fe8-4433-82c4-2b09e410153d"
    },
    {
        "id": "7ca3e58e-68d6-421d-85a5-6513688f382b",
        "description": "Pizzaria Bella Italia",
        "amount": 586.38,
        "type": "expense",
        "date": "2026-09-09",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0"
    },
    {
        "id": "108d5ac3-d945-403a-b775-d5fbd9b159fe",
        "description": "IPTU Parcela",
        "amount": 1414.51,
        "type": "expense",
        "date": "2025-11-18",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2"
    },
    {
        "id": "e7120f57-c611-4198-bc52-72cd5b00e83b",
        "description": "Manutenção do Carro - Troca de Óleo",
        "amount": 966.83,
        "type": "expense",
        "date": "2025-05-14",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "f7119110-d501-4434-83a5-ed75028832c3"
    },
    {
        "id": "82c624c5-d3cf-4f14-8001-a25fb533bcff",
        "description": "Jogos Steam",
        "amount": 19.82,
        "type": "expense",
        "date": "2026-09-25",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd"
    },
    {
        "id": "de75fb4a-7669-436f-814d-aa4d3ce8077d",
        "description": "Exames Laboratoriais",
        "amount": 1370.25,
        "type": "expense",
        "date": "2026-11-17",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f"
    },
    {
        "id": "c33ef8bc-81c8-400e-b138-35723b7da7cc",
        "description": "Adiantamento Salarial / Quinzena",
        "amount": 781.14,
        "type": "income",
        "date": "2025-09-25",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "d924100a-d337-46c2-ad60-78b18a124568"
    },
    {
        "id": "1bbaebea-28ab-4532-b90a-924701da3a0c",
        "description": "Desenvolvimento de Web App - Cliente X",
        "amount": 3002.74,
        "type": "income",
        "date": "2026-01-04",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "b73c62d9-e2ac-4fad-b5f8-f6a58e2fc9a7"
    },
    {
        "id": "25be20df-5b68-417a-94a3-bb848d2bc209",
        "description": "Resgate Parcial Investimentos",
        "amount": 1212.47,
        "type": "income",
        "date": "2025-10-03",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8605b267-eb24-4810-bb60-6d5212b4f50e"
    },
    {
        "id": "5484420e-9654-47fd-a91a-c458fec40bb7",
        "description": "Venda de Item Usado OLX",
        "amount": 4083.8,
        "type": "income",
        "date": "2025-03-22",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8e3de990-a7e0-4935-8b90-0afc65e3241a"
    },
    {
        "id": "559366ff-6e07-43f5-a871-e65210141707",
        "description": "Presente / Transferência Familiar",
        "amount": 842.33,
        "type": "income",
        "date": "2026-04-18",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2870cacd-8fe8-4433-82c4-2b09e410153d"
    },
    {
        "id": "29578192-d7ec-4cca-af77-2bb7f2955fa6",
        "description": "Hortifruti",
        "amount": 607.5,
        "type": "expense",
        "date": "2026-08-17",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0"
    },
    {
        "id": "fd586734-2de4-4663-8f6b-7f82aac32585",
        "description": "Aluguel Residencial",
        "amount": 383.14,
        "type": "expense",
        "date": "2025-06-01",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2"
    },
    {
        "id": "9d1efc6f-7f6b-4884-bda1-9021eaede979",
        "description": "Pedágio AutoBann/ViaOeste",
        "amount": 356.72,
        "type": "expense",
        "date": "2025-01-03",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "f7119110-d501-4434-83a5-ed75028832c3"
    },
    {
        "id": "e9e185f5-7ce9-4d1f-81d9-8a6512a82377",
        "description": "Livro - Livraria Cultura",
        "amount": 115.09,
        "type": "expense",
        "date": "2025-06-03",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd"
    },
    {
        "id": "92529a34-1178-4dff-925a-9bc062a41c97",
        "description": "Farmácia Drogasil",
        "amount": 428.54,
        "type": "expense",
        "date": "2026-04-18",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f"
    },
    {
        "id": "cefcc2db-a4ec-4e79-91fe-d57ea4d02921",
        "description": "Restituição de Imposto de Renda",
        "amount": 2889.53,
        "type": "income",
        "date": "2025-08-26",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "d924100a-d337-46c2-ad60-78b18a124568"
    },
    {
        "id": "cd9fa997-36e5-409f-beb8-075a4788bae9",
        "description": "Consultoria de TI",
        "amount": 489.74,
        "type": "income",
        "date": "2026-06-14",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "b73c62d9-e2ac-4fad-b5f8-f6a58e2fc9a7"
    },
    {
        "id": "8c862c3d-4de9-4676-b0c2-2c9becfabbc3",
        "description": "Rendimento Poupança",
        "amount": 4321.91,
        "type": "income",
        "date": "2025-11-21",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8605b267-eb24-4810-bb60-6d5212b4f50e"
    },
    {
        "id": "7fd95558-f610-4ea5-9c68-ad7af51265fa",
        "description": "Venda Mercado Livre",
        "amount": 2025.05,
        "type": "income",
        "date": "2026-02-08",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8e3de990-a7e0-4935-8b90-0afc65e3241a"
    },
    {
        "id": "30202713-1bc9-4cd5-86c7-f86695596970",
        "description": "Reembolso de Despesas",
        "amount": 2690.7,
        "type": "income",
        "date": "2025-07-06",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2870cacd-8fe8-4433-82c4-2b09e410153d"
    },
    {
        "id": "cfed5ab4-67ff-463c-9ae8-dd901fd1b57c",
        "description": "Supermercado Pão de Açúcar",
        "amount": 385.96,
        "type": "expense",
        "date": "2025-08-26",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0"
    },
    {
        "id": "cde41487-2268-47cf-a01e-4f7e52e87c68",
        "description": "Aluguel Residencial",
        "amount": 90.12,
        "type": "expense",
        "date": "2025-02-25",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2"
    },
    {
        "id": "1af07651-554c-486c-8ff3-09a455807775",
        "description": "Uber Viagem",
        "amount": 618.52,
        "type": "expense",
        "date": "2026-04-28",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "f7119110-d501-4434-83a5-ed75028832c3"
    },
    {
        "id": "ead26837-cdfd-4652-833f-7a4d65d97691",
        "description": "Show / Evento Cultural",
        "amount": 259.49,
        "type": "expense",
        "date": "2025-07-09",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd"
    },
    {
        "id": "39f8c0fa-40ad-4ed0-aa29-9fad3756279b",
        "description": "Farmácia Droga Raia",
        "amount": 643.17,
        "type": "expense",
        "date": "2026-03-07",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f"
    },
    {
        "id": "a668b13c-1565-492e-90f9-f5f500993f9c",
        "description": "Adiantamento Salarial / Quinzena",
        "amount": 4844.17,
        "type": "income",
        "date": "2025-12-11",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "d924100a-d337-46c2-ad60-78b18a124568"
    },
    {
        "id": "ad5c3e10-08c1-4398-adf6-12ce5455c6b1",
        "description": "Desenvolvimento de Web App - Cliente X",
        "amount": 2929.2,
        "type": "income",
        "date": "2025-01-17",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "b73c62d9-e2ac-4fad-b5f8-f6a58e2fc9a7"
    },
    {
        "id": "d5353bb9-bc5c-4be3-baa8-a5161b1fc1a5",
        "description": "Dividendos Ações / FIIs",
        "amount": 361.24,
        "type": "income",
        "date": "2025-11-28",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8605b267-eb24-4810-bb60-6d5212b4f50e"
    },
    {
        "id": "093b6c53-f1b1-4df3-9f66-1853888b47d5",
        "description": "Venda de Item Usado OLX",
        "amount": 617.04,
        "type": "income",
        "date": "2025-10-20",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8e3de990-a7e0-4935-8b90-0afc65e3241a"
    },
    {
        "id": "6a0d7524-fe6f-4c71-a66f-eb8969032f9b",
        "description": "Presente / Transferência Familiar",
        "amount": 428.28,
        "type": "income",
        "date": "2026-05-07",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2870cacd-8fe8-4433-82c4-2b09e410153d"
    },
    {
        "id": "527287a2-7063-48c7-884a-774bab9cac9c",
        "description": "iFood Pedido",
        "amount": 409.44,
        "type": "expense",
        "date": "2025-11-21",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0"
    },
    {
        "id": "cdc21cbd-0a74-49d3-9d3a-59bcd27d531b",
        "description": "Internet Fibra Óptica",
        "amount": 484.52,
        "type": "expense",
        "date": "2025-01-15",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2"
    },
    {
        "id": "b82d0de2-7b05-4504-a209-cfd76ff996e7",
        "description": "Pedágio AutoBann/ViaOeste",
        "amount": 1494.2,
        "type": "expense",
        "date": "2025-09-07",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "f7119110-d501-4434-83a5-ed75028832c3"
    },
    {
        "id": "5f9624c9-0873-4791-8f06-f149f8a8b2f2",
        "description": "Assinatura Netflix",
        "amount": 211.7,
        "type": "expense",
        "date": "2026-02-08",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd"
    },
    {
        "id": "afe46867-82c7-44e7-a859-eece2f72eb5d",
        "description": "Farmácia Droga Raia",
        "amount": 249.25,
        "type": "expense",
        "date": "2026-10-26",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f"
    },
    {
        "id": "b3ad3c24-2e18-4fd2-9709-e5a891c7a42b",
        "description": "Pagamento de Salário Mensal",
        "amount": 3345.96,
        "type": "income",
        "date": "2026-11-04",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "d924100a-d337-46c2-ad60-78b18a124568"
    },
    {
        "id": "6f4a5442-8885-4264-bc4a-3e7be857a15c",
        "description": "Projeto Freelance Frontend",
        "amount": 594.83,
        "type": "income",
        "date": "2025-12-18",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "b73c62d9-e2ac-4fad-b5f8-f6a58e2fc9a7"
    },
    {
        "id": "b8f80aa9-56f0-48f3-9396-77b2440b50d0",
        "description": "Resgate Parcial Investimentos",
        "amount": 1423.15,
        "type": "income",
        "date": "2025-12-11",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8605b267-eb24-4810-bb60-6d5212b4f50e"
    },
    {
        "id": "1c12063d-dde7-4b99-8a43-e90d2e01da35",
        "description": "Venda de Peças / Acessórios",
        "amount": 2536.94,
        "type": "income",
        "date": "2026-01-03",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8e3de990-a7e0-4935-8b90-0afc65e3241a"
    },
    {
        "id": "1ac0882e-f780-49a4-8c3c-97dc90bc2f94",
        "description": "Venda Pontos / Milhas",
        "amount": 239.55,
        "type": "income",
        "date": "2026-03-21",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2870cacd-8fe8-4433-82c4-2b09e410153d"
    },
    {
        "id": "cd3067a6-f039-4f74-b7ee-e9eb7e8e6cf3",
        "description": "Padaria do Bairro",
        "amount": 1115.73,
        "type": "expense",
        "date": "2026-09-01",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0"
    },
    {
        "id": "d0debb52-f533-451d-a9c2-c5025e443b52",
        "description": "Aluguel Residencial",
        "amount": 1418.4,
        "type": "expense",
        "date": "2025-09-02",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2"
    },
    {
        "id": "e8cbae28-ba43-42d4-bcf0-d8e9e9cfcae7",
        "description": "Pedágio AutoBann/ViaOeste",
        "amount": 835.5,
        "type": "expense",
        "date": "2026-03-02",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "f7119110-d501-4434-83a5-ed75028832c3"
    },
    {
        "id": "8c41dd7c-f07c-4672-9eae-7832e6e1b48c",
        "description": "Bar com Amigos",
        "amount": 1349.99,
        "type": "expense",
        "date": "2025-06-07",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd"
    },
    {
        "id": "402b03b7-e851-4e02-93e0-33931251df68",
        "description": "Dentista Limpeza / Tratamento",
        "amount": 167.65,
        "type": "expense",
        "date": "2026-10-24",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f"
    },
    {
        "id": "53f3f4a9-fa4c-49f4-9bf4-d610767f40cd",
        "description": "Adiantamento Salarial / Quinzena",
        "amount": 4325.74,
        "type": "income",
        "date": "2025-07-01",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "d924100a-d337-46c2-ad60-78b18a124568"
    },
    {
        "id": "b5322801-7b0f-42f6-974b-69d39d7c192d",
        "description": "Projeto Freelance Frontend",
        "amount": 3916.28,
        "type": "income",
        "date": "2026-11-28",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "b73c62d9-e2ac-4fad-b5f8-f6a58e2fc9a7"
    },
    {
        "id": "eb6edd2e-8c1b-45a5-8627-b325ac5b3deb",
        "description": "Resgate Parcial Investimentos",
        "amount": 812.81,
        "type": "income",
        "date": "2025-07-28",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8605b267-eb24-4810-bb60-6d5212b4f50e"
    },
    {
        "id": "f3fd5b15-afb6-475e-9edd-bd85a41eba47",
        "description": "Venda de Item Usado OLX",
        "amount": 1127.72,
        "type": "income",
        "date": "2026-06-10",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8e3de990-a7e0-4935-8b90-0afc65e3241a"
    },
    {
        "id": "ef3c6535-aa40-4ad6-82dc-7d8b7c558989",
        "description": "Reembolso de Despesas",
        "amount": 137.85,
        "type": "income",
        "date": "2025-07-11",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2870cacd-8fe8-4433-82c4-2b09e410153d"
    },
    {
        "id": "5e61fdc8-c9a7-403e-bff4-56abe8165d51",
        "description": "Pizzaria Bella Italia",
        "amount": 1450.83,
        "type": "expense",
        "date": "2026-06-21",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0"
    },
    {
        "id": "94c9bbb5-6a10-43c9-96b2-2010840ebd72",
        "description": "Internet Fibra Óptica",
        "amount": 1024.08,
        "type": "expense",
        "date": "2026-01-04",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2"
    },
    {
        "id": "28d77677-082a-4f7f-a822-7c7ca357c1dc",
        "description": "Uber Viagem",
        "amount": 877.18,
        "type": "expense",
        "date": "2026-01-04",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "f7119110-d501-4434-83a5-ed75028832c3"
    },
    {
        "id": "88a076d0-c624-4444-9f0d-5a5171b48ae0",
        "description": "Assinatura Game Pass",
        "amount": 528.35,
        "type": "expense",
        "date": "2026-07-20",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd"
    },
    {
        "id": "5f6c3ea5-984e-4f50-bfd1-327959d385c2",
        "description": "Plano de Saúde Mensalidade",
        "amount": 587.02,
        "type": "expense",
        "date": "2025-05-02",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f"
    },
    {
        "id": "c6fe0282-7796-44c1-bfc0-b8ad88b4c7fd",
        "description": "Pagamento de Salário Mensal",
        "amount": 2609.2,
        "type": "income",
        "date": "2025-06-14",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "d924100a-d337-46c2-ad60-78b18a124568"
    },
    {
        "id": "e2d3325a-5838-4f8b-a103-a738ac914829",
        "description": "Projeto Freelance Frontend",
        "amount": 3123.31,
        "type": "income",
        "date": "2025-12-10",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "b73c62d9-e2ac-4fad-b5f8-f6a58e2fc9a7"
    },
    {
        "id": "69cd9faa-3865-428a-823f-8d3c05215031",
        "description": "Resgate Parcial Investimentos",
        "amount": 3341.13,
        "type": "income",
        "date": "2026-07-23",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8605b267-eb24-4810-bb60-6d5212b4f50e"
    },
    {
        "id": "b666f5f1-368a-46e0-905b-0c60e416ce80",
        "description": "Venda de Equipamento Antigo",
        "amount": 975.36,
        "type": "income",
        "date": "2026-11-24",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8e3de990-a7e0-4935-8b90-0afc65e3241a"
    },
    {
        "id": "ce335b27-0fc7-44b1-a0d9-fef43943944f",
        "description": "Presente / Transferência Familiar",
        "amount": 2854.14,
        "type": "income",
        "date": "2026-09-27",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2870cacd-8fe8-4433-82c4-2b09e410153d"
    },
    {
        "id": "69728656-9ebd-485e-b574-bda34a612a1f",
        "description": "Hortifruti",
        "amount": 441.07,
        "type": "expense",
        "date": "2026-10-20",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0"
    },
    {
        "id": "a14d4efc-9824-486f-8a8c-a40d4219c52f",
        "description": "Internet Fibra Óptica",
        "amount": 671.05,
        "type": "expense",
        "date": "2025-09-16",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2"
    },
    {
        "id": "75093bd0-04e3-4824-860b-3419d8d15a7f",
        "description": "Recarga Cartão Transporte",
        "amount": 140.92,
        "type": "expense",
        "date": "2026-02-27",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "f7119110-d501-4434-83a5-ed75028832c3"
    },
    {
        "id": "f5999708-dde3-4612-94b2-7b3de00c4882",
        "description": "Assinatura Netflix",
        "amount": 348.59,
        "type": "expense",
        "date": "2025-03-01",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd"
    },
    {
        "id": "56bc0692-690b-45bc-b877-7b6d627e469a",
        "description": "Farmácia Drogasil",
        "amount": 1476.14,
        "type": "expense",
        "date": "2025-08-14",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f"
    },
    {
        "id": "0255c1ac-faf5-4343-a943-16090199929a",
        "description": "Adiantamento Salarial / Quinzena",
        "amount": 3597.36,
        "type": "income",
        "date": "2026-08-13",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "d924100a-d337-46c2-ad60-78b18a124568"
    },
    {
        "id": "2035733d-5745-4d5f-822d-915b9c20aa50",
        "description": "Consultoria de TI",
        "amount": 3287.17,
        "type": "income",
        "date": "2025-02-25",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "b73c62d9-e2ac-4fad-b5f8-f6a58e2fc9a7"
    },
    {
        "id": "aa3ea7b1-1a2e-4950-9120-101fe760efbf",
        "description": "Dividendos Ações / FIIs",
        "amount": 895.92,
        "type": "income",
        "date": "2026-01-18",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8605b267-eb24-4810-bb60-6d5212b4f50e"
    },
    {
        "id": "5c4afffe-f362-4b91-b1fc-bb5f2eaa0627",
        "description": "Venda Mercado Livre",
        "amount": 2293.18,
        "type": "income",
        "date": "2026-11-17",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8e3de990-a7e0-4935-8b90-0afc65e3241a"
    },
    {
        "id": "b5e4419f-44bf-4ce3-a152-1c8f988604f4",
        "description": "Presente / Transferência Familiar",
        "amount": 1600.14,
        "type": "income",
        "date": "2026-10-27",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2870cacd-8fe8-4433-82c4-2b09e410153d"
    },
    {
        "id": "a18535b4-99bb-43cf-9533-9bc6bdc9d17b",
        "description": "Burger King",
        "amount": 1248.4,
        "type": "expense",
        "date": "2026-03-24",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8cd39aba-d319-4869-96f0-915ae03cecb0"
    },
    {
        "id": "635708ec-86ec-4390-8d1e-c3de91379600",
        "description": "Internet Fibra Óptica",
        "amount": 399.9,
        "type": "expense",
        "date": "2025-11-09",
        "payment_method": "dinheiro",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "5c6c92f0-c78b-4e66-80c3-d3cf060295a2"
    },
    {
        "id": "9e29d9f2-47c7-4f9f-8cfe-931fb12367dd",
        "description": "Posto Shell - Combustível",
        "amount": 945.72,
        "type": "expense",
        "date": "2026-08-03",
        "payment_method": "debito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "f7119110-d501-4434-83a5-ed75028832c3"
    },
    {
        "id": "c9972d17-923b-41e1-961c-d937f1d0f7a1",
        "description": "Livro - Livraria Cultura",
        "amount": 418.5,
        "type": "expense",
        "date": "2026-09-03",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2ba3bcf3-1539-4ee7-8a3a-6f55707011bd"
    },
    {
        "id": "86084598-13f2-4884-95a1-61bfec23a0bf",
        "description": "Farmácia Drogasil",
        "amount": 358.42,
        "type": "expense",
        "date": "2025-12-07",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "0c67bd29-f92c-4ad1-a9c4-c6a9797d144f"
    },
    {
        "id": "69176677-1ea2-423f-b8c2-926ac8e0b2f7",
        "description": "PLR / Participação nos Lucros",
        "amount": 2049.84,
        "type": "income",
        "date": "2026-07-02",
        "payment_method": "credito",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "d924100a-d337-46c2-ad60-78b18a124568"
    },
    {
        "id": "92367d24-b59c-42c3-9231-76840e4c954a",
        "description": "Manutenção de Sistema - Freelance",
        "amount": 1959.59,
        "type": "income",
        "date": "2025-10-13",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "b73c62d9-e2ac-4fad-b5f8-f6a58e2fc9a7"
    },
    {
        "id": "ed901a49-84dd-4931-bc86-cacf46792e82",
        "description": "Rendimento CDB / Tesouro Direto",
        "amount": 4714.85,
        "type": "income",
        "date": "2026-07-28",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8605b267-eb24-4810-bb60-6d5212b4f50e"
    },
    {
        "id": "85fe7b59-c748-44ea-b880-535976b332d8",
        "description": "Venda de Equipamento Antigo",
        "amount": 2451.38,
        "type": "income",
        "date": "2026-07-16",
        "payment_method": "pix",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "8e3de990-a7e0-4935-8b90-0afc65e3241a"
    },
    {
        "id": "555294ce-33fc-4f25-ab5f-1249a3c76b11",
        "description": "Recebimento de Empréstimo Pessoal",
        "amount": 1693.93,
        "type": "income",
        "date": "2026-12-06",
        "payment_method": "boleto",
        "user_id": "fa8a6508-a7e6-4bad-8125-e0fcc369f9e1",
        "category_id": "2870cacd-8fe8-4433-82c4-2b09e410153d"
    }
]

    stmt_user = db.delete(User)
    
    db.session.execute(stmt_user)
    db.session.commit()

    stm_category = db.delete(Category)
    db.session.execute(stm_category)
    db.session.commit()

    stmt_transaction = db.delete(Transaction)
    db.session.execute(stmt_transaction)
    db.session.commit()

    new_user = User(
        id=UUID(user['id']),
        name=user['name'],
        email=user['email'],
        cpf=user['cpf'],
        phone=user['phone'],
        password_hash=user['password_hash']
    )

    db.session.add(new_user)
    db.session.commit()

    for c in categories:
        new_category = Category(
            id=UUID(c['id']),
            name=c['name'],
            type=c['type'],
            user_id=UUID(c['user_id'])
        )

        db.session.add(new_category)
        db.session.commit()

    for t in transactions:
        new_transaction = Transaction(
            id=UUID(t['id']),
            description=t['description'],
            amount=t['amount'],
            type=t['type'],
            date=datetime.strptime(t['date'], '%Y-%m-%d').date(),
            payment_method=t['payment_method'],
            user_id=UUID(t['user_id']),
            category_id=UUID(t['category_id'])
        )

        db.session.add(new_transaction)
        db.session.commit()