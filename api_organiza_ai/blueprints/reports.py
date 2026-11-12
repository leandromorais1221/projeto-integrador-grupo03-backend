from flask import Blueprint, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from ..wrappers import validate_query
from ..schemas import SummaryQuerySchema, ByCategoryQuerySchema
from ..config.extensions import db
from ..models import Transaction, Category, TransactionType
import openpyxl
from io import BytesIO

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

    start_date_filter = query.startDate
    end_date_filter = query.endDate

    try:
        stmt = select(Transaction.type, func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user_id
        ).group_by(
            Transaction.type
        )

        if start_date_filter:
            stmt = stmt.where(
                Transaction.date >= start_date_filter
            )

        if end_date_filter:
            stmt = stmt.where(
                Transaction.date <= end_date_filter
            )
            
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
            'data': {
              'income': round(income, 2),
              'expense': round(expense, 2),
              'balance': round(balance, 2)
            }
        }), 200
        
    except SQLAlchemyError:
        return jsonify(
            {'message': 'Erro consulte o suporte técnico'}
        ), 500


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
    
    type_filter = query.type
    start_date_filter = query.startDate
    end_date_filter = query.endDate

    try:
        stmt = select(Transaction.category_id, Category.name, func.coalesce(func.sum(Transaction.amount), 0).label('total_amount')).join(
            Category, Transaction.category_id == Category.id
        ).where(
            Transaction.user_id == user_id,
            Transaction.type == type_filter
        ).group_by(
            Transaction.category_id
        ).order_by(
            func.sum(Transaction.amount).desc()
        )

        if start_date_filter:
            stmt = stmt.where(
                Transaction.date >= start_date_filter
            )

        if end_date_filter:
            stmt = stmt.where(
                Transaction.date <= end_date_filter
            )

        results = db.session.execute(stmt).all()

        total_all_amount = sum([float(row.total_amount) for row in results])

        data = []
        for row in results:
            cat_total = float(row.total_amount)
            percentage = (cat_total / total_all_amount * 100) if total_all_amount > 0 else 0.0

            data.append({
                'category_id': str(row.category_id),
                'category_name': row.name,
                'total': round(cat_total, 2),
                'percentage': round(percentage, 2)
            })

        return jsonify({
            'data': data
        }), 200
    
    except SQLAlchemyError:
        return jsonify({'message': 'Erro consulte o suporte técnico'}), 500

@bp.get('/transactions-xlsx')
@jwt_required()
def reports_transactions_pdf():
    """Exporta o relatório de transações do usuário em formato XLSX.

    ---
    tags:
      - Reports

    summary: Exportar transações (XLSX)
    description: >
      Gera e faz o download de um arquivo no formato XLSX contendo todas as
      transações cadastradas pelo usuário autenticado, ordenadas da data mais recente
      para a mais antiga. O identificador do usuário é obtido através do token JWT.

    security:
      - Bearer: []

    produces:
      - application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

    responses:
      200:
        description: Arquivo XLSX gerado e enviado com sucesso como anexo.
        schema:
          type: file
    """

    user_id = UUID(get_jwt_identity())

    stmt = select(Transaction.date, Transaction.description, Category.name, Transaction.type, Transaction.amount).join(
        Category, Transaction.category_id == Category.id
    ).where(
        Transaction.user_id == user_id
    ).order_by(
        Transaction.date.desc()
    )

    transactions = db.session.execute(stmt).all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Relatório de Transações Cadastradas"

    ws['A1'] = 'Data'
    ws['B1'] = 'Descrição'
    ws['C1'] = 'Categoria'
    ws['D1'] = 'Tipo'
    ws['E1'] = 'Valor'

    for transaction in transactions:
        ws.append([transaction.date, transaction.description, transaction.name, 'Receita' if transaction.type == TransactionType.INCOME else 'Despesa', transaction.amount])
        
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="relatorio.xlsx",
        mimetype=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    ), 200




    
    
