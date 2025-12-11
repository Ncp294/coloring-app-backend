from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


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


# define the Template model — represents one table in Postgres
class Template(SQLModel, table=True):
    __tablename__ = "template"  # type: ignore # matches our table name in SQL

    id: int = Field(primary_key=True)
    template_id: str = Field(unique=True)
    user_id: str
    public: bool
    img: str  # placeholder for some sort of image storage
