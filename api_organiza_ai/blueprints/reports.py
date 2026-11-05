from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from ..wrappers import validate_query
from ..schemas import SummaryQuerySchema, ByCategoryQuerySchema
from ..extensions import db
from ..models import Transaction, Category, TransactionType

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.get('/summary')
@jwt_required()
@validate_query(SummaryQuerySchema)
def get_summary(query: SummaryQuerySchema):
    """ Resumo financeiro do usuário (Saldo, Total Receitas e Total Despesas).

    ---
    tags:
    - Reports

    summary: Resumo financeiro (Dashboard)
    description: >
      Calcula totais de receitas, despesas e saldo do usuário autenticado.
      Permite aplicar filtros opcionais de data inicial e final (inclusivos).
      O identificador do usuário é obtido através do token JWT.

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
        description: Data inicial opcional para o filtro no formato YYYY-MM-DD.
        example: "2026-10-01"

      - in: query
        name: endDate
        type: string
        format: date
        required: false
        description: Data final opcional para o filtro no formato YYYY-MM-DD.
        example: "2026-10-31"

    responses:
      200:
        description: Resumo calculado com sucesso.
        examples:
          application/json:
            income: 5200.00
            expense: 3180.45
            balance: 2019.55

      400:
        description: Parâmetros ou formato de data inválidos.
        examples:
          application/json:
            message: Formato de data inválido

      500:
        description: Erro interno ao calcular o resumo financeiro.
        examples:
          application/json:
            message: Erro consulte o suporte técnico
    """
    
    user_id = UUID(get_jwt_identity())

    start_date = query.startDate
    end_date = query.endDate

    try:
        stmt = select(Transaction.type, func.coalesce(func.sum(Transaction.amount), 0)).where(Transaction.user_id == user_id).group_by(Transaction.type)

        if start_date:
            stmt = stmt.where(Transaction.date >= start_date)

        if end_date:
            stmt = stmt.where(Transaction.date <= end_date)
            
        amounts = db.session.execute(stmt).all()

        income = 0.0
        expense = 0.0

        for amount in amounts:
            if amount[0] == TransactionType.INCOME:
                income = float(amount[1])
            elif amount[0] == TransactionType.EXPENSE:
                expense = float(amount[1])

        balance = income - expense

        return jsonify({
            "income": round(income, 2),
            "expense": round(expense, 2),
            "balance": round(balance, 2)
        }), 200
        
    except SQLAlchemyError:
        return jsonify({'message': 'Erro consulte o suporte técnico'}), 500


@bp.get('/by-category')
@jwt_required()
@validate_query(ByCategoryQuerySchema)
def get_by_category(query: ByCategoryQuerySchema):
    """ Relatório de gastos e ganhos agrupados por categoria.

    ---
    tags:
    - Reports

    summary: Resumo por categoria
    description: >
      Agrupa transações do usuário por categoria e calcula a respectiva porcentagem.
      O campo type é obrigatório.
      Permite aplicar intervalos opcionais de data inicial e final (inclusivos).
      O identificador do usuário é obtido através do token JWT.

    security:
      - Bearer: []

    produces:
      - application/json

    parameters:
      - in: query
        name: type
        type: string
        enum:
          - income
          - expense
        required: true
        description: Tipo de transação a ser buscada.
        example: expense

      - in: query
        name: startDate
        type: string
        format: date
        required: false
        description: Data inicial opcional para o filtro no formato YYYY-MM-DD.
        example: "2026-10-01"

      - in: query
        name: endDate
        type: string
        format: date
        required: false
        description: Data final opcional para o filtro no formato YYYY-MM-DD.
        example: "2026-10-31"

    responses:
      200:
        description: Relatório gerado com sucesso.
        examples:
          application/json:
            - category_id: "550e8400-e29b-41d4-a716-446655440000"
              category_name: "Alimentação"
              total: 820.30
              percentage: 41.60

      400:
        description: Parâmetros obrigatórios ausentes ou formato inválido.
        examples:
          application/json:
            message: Parâmetros inválidos

      500:
        description: Erro interno ao gerar o relatório por categoria.
        examples:
          application/json:
            message: Erro consulte o suporte técnico
    """

    user_id = UUID(get_jwt_identity())
    
    type = query.type
    start_date = query.startDate
    end_date = query.endDate

    try:

        # Junta (JOIN) Transação e Categoria, filtra por tipo e usuário, e agrupa somando
        stmt = select(Category.id, Category.name, func.coalesce(func.sum(Transaction.amount), 0).label('total_amount')
        ).join(Transaction, Category.id == Transaction.category_id).where(
            Category.user_id == user_id,
            Transaction.type == type
        ).group_by(
            Category.id, Category.name
        ).order_by(
            func.sum(Transaction.amount).desc()
        )

        if start_date:
            stmt = stmt.where(Transaction.date >= start_date)

        if end_date:
            stmt = stmt.where(Transaction.date <= end_date)

        results = db.session.execute(stmt).all()

        total_geral = sum([float(row.total_amount) for row in results])

        data = []
        for row in results:
            cat_total = float(row.total_amount)
            percentage = (cat_total / total_geral * 100) if total_geral > 0 else 0.0

            data.append({
                'category_id': str(row.id),
                'category_name': row.name,
                'total': round(cat_total, 2),
                'percentage': round(percentage, 2)
            })

        return jsonify(data), 200
    
    except SQLAlchemyError:
        return jsonify({'message': 'Erro consulte o suporte técnico'}), 500