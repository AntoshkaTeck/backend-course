from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility, RoomFacility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User


class HotelDataMapper(DataMapper[HotelsOrm, Hotel]):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper[RoomsOrm, Room]):
    db_model = RoomsOrm
    schema = Room


class RoomWithRelsDataMapper(DataMapper[RoomsOrm, RoomWithRels]):
    db_model = RoomsOrm
    schema = RoomWithRels


class UserDataMapper(DataMapper[UsersOrm, User]):
    db_model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper[BookingsOrm, Booking]):
    db_model = BookingsOrm
    schema = Booking


class FacilityDataMapper(DataMapper[FacilitiesOrm, Facility]):
    db_model = FacilitiesOrm
    schema = Facility


class RoomFacilityDataMapper(DataMapper[RoomsFacilitiesOrm, RoomFacility]):
    db_model = RoomsFacilitiesOrm
    schema = RoomFacility
