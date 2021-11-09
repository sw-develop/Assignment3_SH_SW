from typing import List, Optional, Type

from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.testclient import TestClient

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def test_client():
    client = TestClient(app)
    return client


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/companies", response_model=schemas.CreateCompanyResponse)
def create_company(company: schemas.CreateCompany, x_wanted_language: Optional[str] = Header(None),
                   db: Session = Depends(get_db)):
    company_name_list = []  # CompanyName 객체 임시 생성을 위한 리스트
    for language_name, company_name in company.company_name.items():
        language = crud.get_langauge_by_name(db, language_name)  # language 객체 반환
        company_name_instance = crud.get_company_by_language_and_name(db, language.id, company_name)
        if company_name_instance:  # 해당 객체가 존재하는 경우
            raise HTTPException(status_code=400, detail="Company Name already registered")
        else:
            company_name_instance = models.CompanyName(language_id=language.id,
                                                       name=company_name)  # CompanyName 임시 객체 생성
            company_name_list.append(company_name_instance)

    company_instance = crud.create_company(db)  # Company 객체 반환
    for company_name in company_name_list:
        crud.create_company_name(db, company_instance.id, company_name)  # company_id가 추가된 완전한 CompanyName 객체 생성

    for tag in company.tags:  # tag_name : []안의 {}
        tag_name_dict = list(tag.values())[0]  # {"ko":"" ..}
        for language_name, tag_name in tag_name_dict.items():
            language = crud.get_langauge_by_name(db, language_name)
            crud.create_tag(db, company_instance.id, language.id, tag_name)

    return crud.create_company_response(db, company_instance.id, x_wanted_language)


@app.get("/companies/{company_name}", response_model=schemas.SearchCompany)
def get_company(company_name: str, x_wanted_language: Optional[str] = Header(None), db: Session = Depends(get_db)):
    rtn = crud.get_company(db, company_name, x_wanted_language)
    if rtn is None:
        raise HTTPException(status_code=404)
    return rtn


@app.get("/search/")
def search_company(query: str, x_wanted_language: Optional[str] = Header(None), db: Session = Depends(get_db)):
    print(query)
    return crud.search_company(db, company_name=query, language_key=x_wanted_language)
