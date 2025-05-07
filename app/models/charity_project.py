from sqlalchemy import Column, String, Text

from app.models.abstract import AbstractBase


class CharityProject(AbstractBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
