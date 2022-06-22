# pylint: disable=too-few-public-methods,missing-docstring,invalid-name,no-member

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from blacktape.db import Base


class EntityMatch(Base):
    __tablename__ = "entity"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    label = Column(String)  # Corresponds to spaCy's Span.label_
    offset = Column(Integer)
    file = Column(String)
    file_report_id = Column(Integer, ForeignKey("file_report.id"))

    def __str__(self):
        column_names = [col.key for col in self.__table__.columns]
        return " ".join([f"{name}: {getattr(self, name)}" for name in column_names])


class PatternMatch(Base):
    __tablename__ = "regex"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    pattern = Column(String)
    label = Column(String)  # e.g. "SSN"
    offset = Column(Integer)
    file = Column(String)
    file_report_id = Column(Integer, ForeignKey("file_report.id"))

    def __str__(self):
        column_names = [col.key for col in self.__table__.columns]
        return " ".join([f"{name}: {getattr(self, name)}" for name in column_names])


class FileReport(Base):
    __tablename__ = "file_report"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    name = Column(String)  # for convenience
    size = Column(Integer)
    md5 = Column(String)
    sha256 = Column(String)
    error = Column(String)
    entities = relationship("EntityMatch", backref="file_report")
    regexes = relationship("PatternMatch", backref="file_report")


class Configuration(Base):
    __tablename__ = "configuration"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(String)
