from pydantic import BaseModel, ConfigDict, Field , EmailStr
from decimal import Decimal
from datetime import date
from uuid import UUID
from enum import Enum


class ModelClass(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

class TransactionType(str, Enum):
    INCOME = 'income'
    EXPENSE = 'expense'

class PaymentMethod(str, Enum):
    CREDIT = 'credito'
    DEBIT = 'debito'
    PIX = 'pix'
    CASH = 'dinheiro'
    BOLETO = 'boleto'

class UserSchema(ModelClass):
    name: str = Field(min_length=3)
    cpf: str = Field(min_length=11, max_length=14)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=6)

class LoginSchema(ModelClass):
    email: str
    password: str

class CategorySchema(ModelClass):
    name: str = Field(min_length=3)
    type: TransactionType

class TransactionSchema(ModelClass):
    description: str = Field(min_length=3)
    amount: Decimal = Field(gt=0)
    type: TransactionType
    date: date
    payment_method: PaymentMethod
    category_id: UUID
