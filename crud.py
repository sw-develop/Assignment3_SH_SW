from sqlalchemy.orm import Session

from models         import *
from schemas        import *


def get_company(db: Session, company_name: str, language_key: str):
    language_id = db.query(Language).filter(Language.name == language_key).first().id
    try:
        company_id = db.query(CompanyName).filter(CompanyName.name.contains(company_name)).first().company_id
    except AttributeError:
        return None
    company_name = db.query(CompanyName).filter_by(company_id=company_id, language_id=language_id).first().name
    tags = [tag[0] for tag in db.query(Tag.name).filter_by(company_id=company_id, language_id=language_id).all()]
    return SearchCompany(company_name=company_name, tags=tags)


def search_company(db: Session, company_name: str, language_key: str):
    language_id = db.query(Language).filter(Language.name == language_key).first().id
    company_ids = [company_id[0] for company_id in db.query(CompanyName.company_id)
        .filter(CompanyName.name.contains(company_name)).all()]
    company_names = [dict(company_name=name[0]) for name in
                     db.query(CompanyName.name).filter(CompanyName.company_id.in_(company_ids),
                                                       CompanyName.language_id == language_id).order_by(
                         CompanyName.name.desc()).all()]
    return company_names


def get_company_by_language_and_name(db: Session, language_id: int, company_name: str):
    return db.query(CompanyName).filter(CompanyName.language_id == language_id,
                                        CompanyName.name == company_name).first()


def get_langauge_by_name(db: Session, language_name: str):
    language = db.query(Language).filter(Language.name == language_name).first()
    if language:
        return language
    else:
        return create_language(db, language_name)


def create_language(db: Session, language_name: str):
    language = Language(name=language_name)
    db.add(language)
    db.commit()
    db.refresh(language)
    return language


def create_company(db: Session):
    company = Company()
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def create_company_name(db: Session, company_id: int, company_name: CompanyName):
    company_name.company_id = company_id
    db.add(company_name)
    db.commit()
    db.refresh(company_name)


def create_tag(db: Session, company_id: int, language_id: int, tag_name: str):
    tag = Tag(company_id=company_id, language_id=language_id, name=tag_name)
    db.add(tag)
    db.commit()
    db.refresh(tag)


def get_company_by_language_and_company(db, language_id, company_id):
    return db.query(CompanyName).filter(CompanyName.language_id == language_id,
                                        CompanyName.company_id == company_id).first()


def get_tag_list_by_language_and_company(db, language_id, company_id):
    tags = db.query(Tag).filter(Tag.language_id == language_id,
                                Tag.company_id == company_id).all()  # queryset 반환

    tag_list = []
    for tag in tags:
        tag_list.append(tag.name)
    return tag_list


def create_company_response(db: Session, company_id: int, x_wanted_language: str):
    language_id = get_langauge_by_name(db, x_wanted_language).id
    company_name = get_company_by_language_and_company(db, language_id, company_id).name
    tags = get_tag_list_by_language_and_company(db, language_id, company_id)

    return CreateCompanyResponse(company_name=company_name, tags=tags)
