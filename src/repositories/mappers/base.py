from typing import TypeVar, Generic

from pydantic import BaseModel

from src.database import Base

DBModel = TypeVar("DBModel", bound=Base)
Schema = TypeVar("Schema", bound=BaseModel)


class DataMapper(Generic[DBModel, Schema]):
    db_model: type[DBModel]
    schema: type[Schema]

    @classmethod
    def map_to_domain_entity(cls, data: DBModel) -> Schema:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: Schema) -> DBModel:
        return cls.db_model(**data.model_dump())
