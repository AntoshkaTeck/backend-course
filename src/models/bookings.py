from datetime import date

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from src.database import Base


class BookingsOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    date_from: Mapped[date] = mapped_column()
    date_to: Mapped[date] = mapped_column()
    price: Mapped[int] = mapped_column()

    @hybrid_property
    def total_cost(self):
        return self.price * (self.date_from - self.date_to).days
