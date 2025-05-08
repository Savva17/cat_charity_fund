from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest_close_date(obj_in):
    if obj_in.invested_amount == obj_in.full_amount:
        obj_in.fully_invested = True
        obj_in.close_date = datetime.utcnow()


async def invest(
        source: Union[CharityProject, Donation],
        db_objs: list[Union[CharityProject, Donation]],
        session: AsyncSession
):
    for db_obj in db_objs:
        if source.fully_invested:
            break

        source_available = source.full_amount - source.invested_amount
        db_obj_need = db_obj.full_amount - db_obj.invested_amount
        min_amount = min(source_available, db_obj_need)

        source.invested_amount += min_amount
        db_obj.invested_amount += min_amount

        await invest_close_date(source)
        await invest_close_date(db_obj)

        session.add(db_obj)


async def investment_donation(
        donation: Donation,
        session: AsyncSession
):
    projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested.is_(False)
        ).order_by(CharityProject.create_date)
    )
    projects = projects.scalars().all()

    await invest(donation, projects, session)

    session.add(donation)
    await session.commit()
    await session.refresh(donation)
    return donation


async def investment_project(
        project: CharityProject,
        session: AsyncSession
):
    donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested.is_(False)
        ).order_by(Donation.create_date)
    )
    donations = donations.scalars().all()

    await invest(project, donations, session)

    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project
