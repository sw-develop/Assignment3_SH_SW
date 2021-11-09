from sqlalchemy.orm import Session

import models, schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
#
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
#
#
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
#
#
# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
#
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

def get_company_by_language_and_name(db: Session, language_id: int, company_name: str):
    return db.query(models.CompanyName).filter(models.CompanyName.language_id == language_id,
                                               models.CompanyName.name == company_name).first()


def get_langauge_by_name(db: Session, language_name: str):
    language = db.query(models.Language).filter(models.Language.name == language_name).first()
    if language:
        return language
    else:
        return create_language(db, language_name)


def create_language(db: Session, language_name: str):
    language = models.Language(name=language_name)
    db.add(language)
    db.commit()
    db.refresh(language)
    return language


def create_company(db: Session):
    company = models.Company()
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def create_company_name(db: Session, company_id: int, company_name: models.CompanyName):
    company_name.company_id = company_id
    db.add(company_name)
    db.commit()
    db.refresh(company_name)


def create_tag(db: Session, company_id: int, language_id: int, tag_name: str):
    tag = models.Tag(company_id=company_id, language_id=language_id, name=tag_name)
    db.add(tag)
    db.commit()
    db.refresh(tag)


def get_company_by_language_and_company(db, language_id, company_id):
    return db.query(models.CompanyName).filter(models.CompanyName.language_id == language_id,
                                               models.CompanyName.company_id == company_id).first()


def get_tag_list_by_language_and_company(db, language_id, company_id):
    tags = db.query(models.Tag).filter(models.Tag.language_id == language_id,
                                       models.Tag.company_id == company_id).all()  # queryset 반환

    tag_list = []
    for tag in tags:
        tag_list.append(tag.name)
    return tag_list


def create_company_response(db: Session, company_id: int, x_wanted_language: str):
    language_id = get_langauge_by_name(db, x_wanted_language).id
    company_name = get_company_by_language_and_company(db, language_id, company_id).name
    tags = get_tag_list_by_language_and_company(db, language_id, company_id)

    return schemas.CreateCompanyResponse(company_name=company_name, tags=tags)
