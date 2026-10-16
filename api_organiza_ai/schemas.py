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
    name: str = Field(ge=3)
    cpf: str = Field(ge=11, le=14)
    email: EmailStr
    phone: str = Field(ge=10, le=15)
    password: str = Field(ge=6)

class CategorySchema(BaseModel):
    name: str = Field(ge=3)
    type: TransactionType

class TransactionSchmea(BaseModel):
    description: str = Field(ge=3)
    amount: Decimal
    type: TransactionType
    date: date
    payment_method: PaymentMethod
    category_id: UUID
