from src.models.facilities import FacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facility import Facility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility