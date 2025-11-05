from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int = Field(..., ge=1, le=2_147_483_647)


class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
