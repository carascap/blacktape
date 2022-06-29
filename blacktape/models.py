# pylint: disable=too-few-public-methods,missing-docstring,invalid-name,no-member

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from blacktape.db import Base


class Match(Base):
    __tablename__ = "match"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # "regex" or "entity"
    text = Column(String)
    pattern = Column(String)  # regex only
    label = Column(
        String
    )  # spaCy's Span.label_ for entities, custom for regexes (e.g. "SSN")
    offset = Column(Integer)
    file = Column(String)
    file_report_id = Column(Integer, ForeignKey("file_report.id"))

    def __str__(self):
        column_names = [col.key for col in self.__table__.columns]
        return "\n".join([f"{name}: {getattr(self, name)}" for name in column_names])


class FileReport(Base):
    __tablename__ = "file_report"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    matches = relationship("Match", backref="file_report")


class Configuration(Base):
    __tablename__ = "configuration"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(String)
