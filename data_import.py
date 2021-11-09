import csv
from models     import *
from database   import SessionLocal

db = SessionLocal()


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def make_object(row, **kwargs):
    com = Company()
    db.add(com)
    db.commit()
    db.refresh(com)
    company_names = []
    ko_tags = []
    en_tags = []
    ja_tags = []
    for i in range(0, 3):
        if row[i]:
            company_names.append(CompanyName(name=row[i], language_id=kwargs.get(f'{i}'), company_id=com.id))
    if row[3]:
        tags = row[3].split('|')
        for t in tags:
            ko_tags.append(Tag(name=t, language_id=kwargs.get('0'), company_id=com.id))
    if row[4]:
        tags = row[4].split('|')
        for t in tags:
            en_tags.append(Tag(name=t, language_id=kwargs.get('1'), company_id=com.id))
    if row[5]:
        tags = row[5].split('|')
        for t in tags:
            ja_tags.append(Tag(name=t, language_id=kwargs.get('2'), company_id=com.id))
    return company_names, ko_tags, en_tags, ja_tags


def import_data(file):
    f = open(file, 'r', encoding='utf-8')
    rdr = list(csv.reader(f))

    ko = get_or_create(db, Language, **dict(name="ko")).id
    en = get_or_create(db, Language, **dict(name="en")).id
    jp = get_or_create(db, Language, **dict(name="jp")).id

    language_ids = {
        "0": ko,
        "1": en,
        "2": jp
    }

    for i in range(1, len(rdr)):
        company_names, ko_tags, en_tags, ja_tags = make_object(rdr[i], **language_ids)
        db.bulk_save_objects(company_names)
        db.commit()
        db.bulk_save_objects(ko_tags)
        db.commit()
        db.bulk_save_objects(en_tags)
        db.commit()
        db.bulk_save_objects(ja_tags)
        db.commit()
