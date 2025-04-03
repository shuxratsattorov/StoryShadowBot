import datetime
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy import func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

inpk = Annotated[int, mapped_column(primary_key=True, index=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=func.now(), onupdate=datetime.datetime.now())]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[inpk]
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    fullname: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    banned: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class Search(Base):
    __tablename__ = "searches"

    id: Mapped[inpk]
    search: Mapped[str] = mapped_column(nullable=True)
    count: Mapped[int] = mapped_column(default=1)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))