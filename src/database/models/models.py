from typing import Dict, Any
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    JSON,
    Date, 
    String, 
    Integer, 
    Boolean, 
    DateTime,
    ForeignKey, 
    BigInteger, 
    LargeBinary, 
)

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


class DeviceInfo(Base):
    __tablename__ = "device_info"

    title: Mapped[str] = mapped_column(String, nullable=True)
    device_settings: Mapped[Dict[str, Any]] = mapped_column(JSON)

    acoounts: Mapped[list["InstagramAccount"]] = relationship("InstagramAccount", back_populates="device")


class InstagramAccount(Base):
    __tablename__ = "instagram_accounts"

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    device_id: Mapped[int] = mapped_column(ForeignKey("device_info.id"))
    
    device: Mapped["DeviceInfo"] = relationship("DeviceInfo", backref="accounts")
    sessions: Mapped[list["InstagramSession"]] = relationship("InstagramSession", back_populates="account")


class InstagramSession(Base):
    __tablename__ = "instagram_sessions"

    session_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    proxy: Mapped[str] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_valid: Mapped[bool] = mapped_column(Boolean, default=True)
    is_on_cooldown: Mapped[bool] = mapped_column(Boolean, default=False)

    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    daily_usage_count: Mapped[int] = mapped_column(String, default=0)
    last_used_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    cooldown_until: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    refreshed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    last_error: Mapped[str] = mapped_column(String, nullable=True)

    account_id: Mapped[int] = mapped_column(ForeignKey("instagram_accounts.id"), nullable=False)
    account: Mapped["InstagramAccount"] = relationship("InstagramAccount", back_populates="sessions")