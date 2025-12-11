from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field


class Dependency(BaseModel):
    service: str
    status: str
    response_time_ms: int


class HealthData(BaseModel):
    service: str
    status: str
    dependencies: Optional[list[Dependency]]


class Template(BaseModel):
    id: int = Field(primary_key=True)
    template_id: str = Field(unique=True)
    user_id: str
    public: bool
    img: str  # placeholder for some sort of image storage
