from pydantic import BaseModel, Field , EmailStr
from decimal import Decimal
from datetime import date
from uuid import UUID
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

class UserSchema(BaseModel):
    name: str = Field(min_length=3)
    cpf: str = Field(min_length=11, max_length=14)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=6)

class CategorySchema(BaseModel):
    name: str = Field(min_length=3)
    type: TransactionType

class TransactionSchema(BaseModel):
    description: str = Field(min_length=3)
    amount: Decimal
    type: TransactionType
    date: date
    payment_method: PaymentMethod
    category_id: UUID
