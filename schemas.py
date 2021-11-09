from typing     import List, Optional

from pydantic   import BaseModel


class SearchCompany(BaseModel):
    company_name: str
    tags: List[str] = []


class CreateCompany(BaseModel):
    company_name: dict
    tags: List[dict] = []


class CompanyNameSchema(BaseModel):
    company_name: str


class AutoCompleteCompany(BaseModel):
    company_name: str
    description: Optional[str] = None


class CreateCompanyResponse(BaseModel):
    company_name: str
    tags: List[str] = []

    class Config:
        orm_mode = True
