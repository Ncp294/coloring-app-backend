from typing import Optional

from pydantic import BaseModel


class Dependency(BaseModel):
    service: str
    status: str
    response_time_ms: int


class HealthData(BaseModel):
    service: str
    status: str
    dependencies: Optional[list[Dependency]]


class TemplateCreate(BaseModel):
    template_id: str
    user_id: str
    public: bool
    img: str  # placeholder for some sort of image storage


class TemplateResponse(BaseModel):
    template_id: str
    user_id: str
    public: bool
    img: str  # placeholder for some sort of image storage
