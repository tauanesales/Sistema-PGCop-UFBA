from datetime import date

from sqlalchemy import Date, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class BaseModel(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData()

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, index=True)
    created_at: Mapped[date] = mapped_column(
        Date(), default=func.utcnow(), nullable=False
    )
    updated_at: Mapped[date] = mapped_column(
        Date(), default=func.utcnow(), nullable=False, onupdate=func.utcnow()
    )
    deleted_at: Mapped[date] = mapped_column(Date(), nullable=True)
