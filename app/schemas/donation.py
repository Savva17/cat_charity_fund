from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.models.user import User


class DonationBase(BaseModel):
    full_amount: int = Field(
        ...,
        gt=0,
        title='Сумма пожертвования'
    )
    comment: Optional[str] = Field(None, title='Комментарий')

    class Config:
        schema_extra = {
            'example': {
                'full_amount': 50,
                'comment': 'Комментарий'
            }
        }


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int]
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
