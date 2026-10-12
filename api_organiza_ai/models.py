import enum
import uuid
from decimal import Decimal
from datetime import datetime, date as TypeDate
from sqlalchemy import String, DateTime, Date, Numeric, ForeignKey, Uuid
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db


class TransactionType(str, enum.Enum):
    INCOME = 'income'
    EXPENSE = 'expense'

class PaymentMethod(str, enum.Enum):
    CREDIT = 'credito'
    DEBIT = 'debito'
    PIX = 'pix'
    CASH = 'dinheiro'
    BOLETO = 'boleto'


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    cpf: Mapped[str] = mapped_column(String(14), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(15))
    
    password_hash: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    categories: Mapped[list["Category"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.email}>'


class Category(db.Model):
    __tablename__ = 'categories'

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType))

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")

    def __repr__(self):
        return f'<Category {self.name} ({self.type})>'


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description: Mapped[str] = mapped_column(String(200)) 
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType))
    date: Mapped[TypeDate] = mapped_column(Date) 
    payment_method: Mapped[PaymentMethod] = mapped_column(SQLEnum(PaymentMethod))
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('categories.id'))

    user: Mapped["User"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship(back_populates="transactions")

    def __repr__(self):
        return f'<Transaction {self.description} $ {self.amount}>'