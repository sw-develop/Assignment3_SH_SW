from datetime       import datetime

from sqlalchemy     import Column, ForeignKey, Integer, String, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship

from database       import Base


# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
#
#     items = relationship("Item", back_populates="owner")
#
#
# class Item(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#
#     owner = relationship("User", back_populates="items")
#

class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    tags = relationship("Tag", back_populates="language")
    company_names = relationship("CompanyName", back_populates="language")


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    tags = relationship("Tag", back_populates="company")
    company_names = relationship("CompanyName", back_populates="company")


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("company.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    company = relationship("Company", back_populates="tags")
    language = relationship("Language", back_populates="tags")

    name = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class CompanyName(Base):
    __tablename__ = "company_name"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("company.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    company = relationship("Company", back_populates="company_names")
    language = relationship("Language", back_populates="company_names")

    name = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('language_id', 'name', name='_language_companyname_uc'),)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
