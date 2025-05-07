from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.process_invest import investment_donation

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Возвращает список всех пожертвований'
)
async def get_all_danation(
    session: AsyncSession = Depends(get_async_session)
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={'user_id', 'fully_invested', 'invested_amount'},
    summary='Сделать пожертвование'
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_donation = await donation_crud.create(donation, session)
    new_donation = await investment_donation(
        donation=new_donation, session=session)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    response_model_exclude={'user_id', 'fully_invested', 'invested_amount'},
    summary='Список пожертвований пользователя'
)
async def get_my_donation(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список пожертвований пользователя."""
    user_donation = await donation_crud.get_user_donation(user, session)
    return user_donation
