from typing import Optional

from sqlmodel import Field, SQLModel

# CategoryBase class (no  SQL table)
class CategoryBase(SQLModel):
    name: str = Field(min_length=3, max_length=15, index=True)

# Category class (and SQL table) inherits from 
class Category(CategoryBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)