from datetime import datetime

from sqlalchemy import Date
from sqlalchemy import ForeignKey, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    fullname: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    daily_download_date: Mapped[datetime] = mapped_column(Date, nullable=True)
    daily_download_count: Mapped[int] = mapped_column(Integer, default=0)


class Referral(Base):
    __tablename__ = 'referrals'

    referred_user: Mapped[int] = mapped_column(BigInteger, unique=True)
    flag: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))


class Search(Base):
    __tablename__ = "searches"

    search: Mapped[str] = mapped_column(nullable=True)
    count: Mapped[int] = mapped_column(default=1)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))


class AutoFetchStories(Base):
    __tablename__ = "auto_fetch_stories"

    account: Mapped[str] = mapped_column(nullable=True)
    last_time: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))


class MonitorAccountStatus(Base):
    __tablename__ = "monitor_account_status"

    account: Mapped[str] = mapped_column(nullable=True)
    was_private: Mapped[bool] = mapped_column(default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", onupdate="CASCADE"))