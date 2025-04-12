from datetime import date
from typing import Annotated

from sqlalchemy import ForeignKey, Date, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, updated_at


inpk = Annotated[int, mapped_column(primary_key=True, index=True)]


class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    fullname: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    daily_download_date: Mapped[updated_at]
    daily_download_count: Mapped[int] = mapped_column(Integer, default=0)


class Referral(Base):
    __tablename__ = 'referrals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referred_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.tg_id'))
    referrer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.tg_id'))

    # Foydalanuvchilar bilan aloqalar
    referred_user: Mapped["User"] = relationship("User", foreign_keys=[referred_user_id], backref="referred_by")
    referrer: Mapped["User"] = relationship("User", foreign_keys=[referrer_id], back_populates="referrals")


class Search(Base):
    __tablename__ = "searches"

    search: Mapped[str] = mapped_column(nullable=True)
    count: Mapped[int] = mapped_column(default=1)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))


class FollowAccount(Base):
    __tablename__ = "follow_account"

    account: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))


class Notification(Base):
    __tablename__ = "notification"

    account: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", onupdate="CASCADE"))