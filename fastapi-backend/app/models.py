from datetime import datetime

from pydantic import UUID4, BaseModel, Field


class CustomerRequest(BaseModel):
    type_: str = Field(..., alias="type", min_length=1, max_length=256)
    salesforce_id: None | str = Field(None, min_length=1, max_length=256)
    registration_platform: str = Field(..., min_length=1, max_length=256)
    created_by: str = Field(..., min_length=1, max_length=256)


class CustomerOut(BaseModel):
    uid: UUID4
    type_: str = Field(..., alias="type")
    registration_date: datetime
    salesforce_id: None | str
    registration_platform: str
    created_by: str


class CustomerResponse(CustomerOut):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
