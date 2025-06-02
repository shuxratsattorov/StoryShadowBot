from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class Payment(Base):
    __tablename__ = 'payments'

    pay_id: Mapped[int] = mapped_column()
    type: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))