from enum import Enum

class TransactionType(str, Enum):
    INCOME = 'income'
    EXPENSE = 'expense'

class PaymentMethod(str, Enum):
    CREDIT = 'credito'
    DEBIT = 'debito'
    PIX = 'pix'
    CASH = 'dinheiro'
    BOLETO = 'boleto'
