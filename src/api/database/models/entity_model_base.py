from datetime import date, datetime

from sqlalchemy import Date, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class EntityModelBase(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData()

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, index=True)
    created_at: Mapped[date] = mapped_column(
        Date(), default=datetime.utcnow(), nullable=False
    )
    updated_at: Mapped[date] = mapped_column(
        Date(), default=datetime.utcnow(), nullable=False, onupdate=datetime.utcnow
    )
    deleted_at: Mapped[date] = mapped_column(Date(), nullable=True)
