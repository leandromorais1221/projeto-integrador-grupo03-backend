import enum
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, Float, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .extensions import db

class TipoMovimentacao(str, enum.Enum):
    RECEITA = 'receita'
    DESPESA = 'despesa'

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(256))
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    categorias: Mapped[List["Categoria"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    transacoes: Mapped[List["Transacao"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Usuario {self.email}>'


class Categoria(db.Model):
    __tablename__ = 'categorias'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50)) #lazer, trasporte, etc...
    tipo: Mapped[TipoMovimentacao] = mapped_column(SQLEnum(TipoMovimentacao)) 
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'))

    usuario: Mapped["Usuario"] = relationship(back_populates="categorias")
    transacoes: Mapped[List["Transacao"]] = relationship(back_populates="categoria")

    def __repr__(self):
        return f'<Categoria {self.nome} ({self.tipo})>'

class Transacao(db.Model):
    __tablename__ = 'transacoes'

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[Optional[str]] = mapped_column(String(200)) 
    valor: Mapped[float] = mapped_column(Float)
    tipo: Mapped[TipoMovimentacao] = mapped_column(SQLEnum(TipoMovimentacao))
    data: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    metodo_pagamento: Mapped[Optional[str]] = mapped_column(String(50))  # Opcional
    # Chaves estrangeiras
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'))
    categoria_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categorias.id'))

    usuario: Mapped["Usuario"] = relationship(back_populates="transacoes")
    categoria: Mapped[Optional["Categoria"]] = relationship(back_populates="transacoes")

    def __repr__(self):
        return f'<Transacao {self.descricao} R$ {self.valor}>'