from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.get("/companies/{company_name}")
def get_company(company_name: str):
    pass


@app.get("/search/")
def search_company(query: str):
    pass


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)
#
#
# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
#
#
# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
def test_client():
    client = TestClient(app)
    return client
