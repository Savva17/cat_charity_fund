from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator, Field, Extra


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title='Название проекта'
    )
    description: str = Field(
        ...,
        min_length=1,
        title='Описание проекта'
    )
    full_amount: int = Field(
        ...,
        gt=0,
        title='Требуемая сумма'
    )

    class Config:
        schema_extra = {
            'example': {
                'name': 'Project 1',
                'description': 'Description for project.',
                'full_amount': 100
            }
        }

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value == '' or value is None:
            raise ValueError('Название проекта не может быть пустым.')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value):
        if value == '' or value is None:
            raise ValueError('Описание проекта не может быть пустым.')
        return value

    @validator('full_amount')
    def full_amount_cannot_be_less_than_zero(cls, value):
        if value < 0:
            raise ValueError('Сумма проекта не может быть меньше 0.')
        return value


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        title='Название проекта'
    )
    description: Optional[str] = Field(
        None,
        min_length=1,
        title='Описание проекта'
    )
    full_amount: Optional[int] = Field(
        None,
        gt=0,
        title='Требуемая сумма'
    )

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = Field(
        0,
        title='Внесённая сумма'
    )
    fully_invested: bool = Field(
        default=False
    )
    create_date: datetime = Field(default_factory=datetime.utcnow)
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
