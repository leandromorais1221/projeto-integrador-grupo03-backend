from pydantic import BaseModel, ConfigDict, Field , EmailStr
from decimal import Decimal
from datetime import date
from uuid import UUID
from .enums import TransactionType, PaymentMethod


class ModelClass(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

class UserSchema(ModelClass):
    name: str = Field(min_length=3, max_length=120)
    cpf: str = Field(min_length=11, max_length=14)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=6)

class LoginSchema(ModelClass):
    email: str
    password: str

class CategorySchema(ModelClass):
    name: str = Field(min_length=3, max_length=50)
    type: TransactionType

class TransactionSchema(ModelClass):
    description: str = Field(min_length=3, max_length=200)
    amount: Decimal = Field(gt=0)
    type: TransactionType
    date: date
    payment_method: PaymentMethod
    category_id: UUID

class TranscationsQuerySchema(ModelClass):
    search: str | None = None
    startDate: date | None = None
    endDate: date | None = None
    categoryId: UUID | None = None
    type: TransactionType | None = None
    minAmount: Decimal | None = Field(gt=0, default=None)
    maxAmount: Decimal | None = Field(gt=0, default=None)

class SummaryQuerySchema(ModelClass):
    startDate: date | None = None
    endDate: date | None = None

class ByCategoryQuerySchema(ModelClass):
    type: TransactionType
    startDate: date | None = None
    endDate: date | None = None
