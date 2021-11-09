from typing import List, Optional

from pydantic import BaseModel


class SearchCompany(BaseModel):
    company_name: str
    tags: List[str] = []


class CreateCompany(BaseModel):
    company_name: dict
    tags: List[dict] = []
# class AutoCompleteCompany(BaseModel):
#     company_name: str
#     description: Optional[str] = None

# class ItemCreate(ItemBase):
#     pass
#
#
# class Item(ItemBase):
#     id: int
#     owner_id: int
#
#     class Config:
#         orm_mode = True
#
#
# class UserBase(BaseModel):
#     email: str
#
#
# class UserCreate(UserBase):
#     password: str
#
#
# class User(UserBase):
#     id: int
#     is_active: bool
#     items: List[Item] = []
#
#     class Config:
#         orm_mode = True