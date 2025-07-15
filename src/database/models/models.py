from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, BigInteger, String, Integer, Boolean, LargeBinary, Date

from src.database.base import Base


class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    fullname: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    language: Mapped[str] = mapped_column(nullable=True)
    daily_download_date: Mapped[datetime] = mapped_column(Date, nullable=True)
    daily_download_count: Mapped[int] = mapped_column(Integer, default=0)


class Search(Base):
    __tablename__ = "searches"

    search: Mapped[str] = mapped_column(String, nullable=True)
    count: Mapped[int] = mapped_column(Integer, default=1)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))


class AutoFetchStories(Base):
    __tablename__ = "auto_fetch_stories"

    account: Mapped[str] = mapped_column(String, nullable=True)
    last_time: Mapped[datetime] = mapped_column(Date, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))


class MonitorAccountStatus(Base):
    __tablename__ = "monitor_account_status"

    account: Mapped[str] = mapped_column(String, nullable=True)
    was_private: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", onupdate="CASCADE"))


class InstagramSession(Base):
    __tablename__ = "instagram_sessions"

    account: Mapped[str] = mapped_column(String)
    session: Mapped[bytes] = mapped_column(LargeBinary)


class InstaramAccount(Base):
    __tablename__ = "instagram_accounts"

    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    status: Mapped[bool] = mapped_column(Boolean, default=False)