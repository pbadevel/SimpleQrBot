from dataclasses import dataclass
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IDSchema(Schema):
    id: Annotated[int, Field(gt=0, description="The ID of the object.")]


class TimestampedSchema(Schema):
    created_at: Annotated[
        datetime, Field(description="Creation timestamp of the object.")
    ]
    updated_at: Annotated[
        datetime, Field(description="Last modification timestamp of the object.")
    ]


@dataclass(slots=True)
class ClassName:
    """
    Used as an annotation metadata, it allows us to customize the name generated
    by Pydantic for a type; in particular, a long union.

    It does **nothing** on its own, but it can be used by other classes.

    Currently, it's used by `ListResource` to generate a shorter name for the
    OpenAPI schema, when we list a resource having a long union type.
    """

    name: str

    def __hash__(self) -> int:
        return hash(type(self.name))
