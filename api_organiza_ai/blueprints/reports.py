from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from datetime import datetime

from ..extensions import db
from ..models import Transaction, Category, TransactionType

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.get('/summary')
@jwt_required()
def get_summary():
    """ Resumo financeiro do usuário (Saldo, Total Receitas e Total Despesas).

    ---
    tags:
      - Reports
    summary: Resumo financeiro (Dashboard)
    description: >
      Calcula totais de receitas, despesas e saldo.
      Filtros opcionais de data (inclusivos).
    security:
      - Bearer: []
    produces:
      - application/json
    parameters:
      - in: query
        name: startDate
        type: string
        format: date
        required: false
        description: Data inicial (YYYY-MM-DD).
      - in: query
        name: endDate
        type: string
        format: date
        required: false
        description: Data final (YYYY-MM-DD).
    responses:
      200:
        description: Resumo calculado com sucesso.
        examples:
          application/json:
            income: 5200.00
            expense: 3180.45
            balance: 2019.55
      400:
        description: Formato de data inválido.
      500:
        description: Erro interno.
    """
    user_id = UUID(get_jwt_identity())
    start_date_str = request.args.get('startDate')
    end_date_str = request.args.get('endDate')

    try:
        stmt = select(
            Transaction.type, 
            func.coalesce(func.sum(Transaction.amount), 0)
        ).where(Transaction.user_id == user_id).group_by(Transaction.type)

        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            stmt = stmt.where(Transaction.date >= start_date)
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            stmt = stmt.where(Transaction.date <= end_date)

        results = db.session.execute(stmt).all()

        income = 0.0
        expense = 0.0

        for row in results:
            if row[0] == TransactionType.INCOME:
                income = float(row[1])
            elif row[0] == TransactionType.EXPENSE:
                expense = float(row[1])

        balance = income - expense

        return jsonify({
            "income": round(income, 2),
            "expense": round(expense, 2),
            "balance": round(balance, 2)
        }), 200

    except ValueError:
        return jsonify({'message': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    except SQLAlchemyError:
        return jsonify({'message': 'Erro consulte o suporte técnico'}), 500


@bp.get('/by-category')
@jwt_required()
def get_by_category():
    """ Relatório de gastos e ganhos agrupados por categoria.

    ---
    tags:
      - Reports
    summary: Resumo por categoria
    description: >
      Agrupa transações do usuário por categoria e calcula a porcentagem.
      Filtro de tipo (padrão: expense) e datas opcionais.
    security:
      - Bearer: []
    produces:
      - application/json
    parameters:
      - in: query
        name: type
        type: string
        enum: [income, expense]
        required: false
        description: Tipo de transação a ser buscada (Padrão = expense).
      - in: query
        name: startDate
        type: string
        format: date
        required: false
      - in: query
        name: endDate
        type: string
        format: date
        required: false
    responses:
      200:
        description: Relatório gerado com sucesso.
        examples:
          application/json:
            - categoryId: "c1a2..."
              categoryName: "Alimentação"
              total: 820.30
              percentage: 41.60
      400:
        description: Formato de data inválido.
      500:
        description: Erro interno.
    """
    user_id = UUID(get_jwt_identity())
    
    tx_type_str = request.args.get('type', 'expense')
    start_date_str = request.args.get('startDate')
    end_date_str = request.args.get('endDate')

    try:
        tx_type = TransactionType.INCOME if tx_type_str == 'income' else TransactionType.EXPENSE

        # Junta (JOIN) Transação e Categoria, filtra por tipo e usuário, e agrupa somando
        stmt = select(
            Category.id,
            Category.name,
            func.coalesce(func.sum(Transaction.amount), 0).label('total_amount')
        ).join(
            Transaction, Category.id == Transaction.category_id
        ).where(
            Category.user_id == user_id,
            Transaction.type == tx_type
        ).group_by(
            Category.id, Category.name
        ).order_by(
            func.sum(Transaction.amount).desc()  # Contrato pede array ordenado por total desc
        )

        # Aplica os filtros de data
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            stmt = stmt.where(Transaction.date >= start_date)
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            stmt = stmt.where(Transaction.date <= end_date)

        results = db.session.execute(stmt).all()

        total_geral = sum([float(row.total_amount) for row in results])

        data = []
        for row in results:
            cat_total = float(row.total_amount)
            percentage = (cat_total / total_geral * 100) if total_geral > 0 else 0.0

            data.append({
                "categoryId": str(row.id),
                "categoryName": row.name,
                "total": round(cat_total, 2),
                "percentage": round(percentage, 2)
            })

        return jsonify(data), 200

    except ValueError:
        return jsonify({'message': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    except SQLAlchemyError:
        return jsonify({'message': 'Erro consulte o suporte técnico'}), 500