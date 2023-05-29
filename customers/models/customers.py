from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from server.db import CustomerBase


class Customer(CustomerBase):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    phone: Mapped[str] = mapped_column(String(10), unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Customer(id={self.id!r}, name={self.name!r}, phone={self.phone!r})"
