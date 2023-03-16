from typing import Optional

from sqlmodel import Field, SQLModel

class Category(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(min_length=3, max_length=15, index=True)