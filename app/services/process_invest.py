from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.charity_project import CharityProject
from app.models.donation import Donation


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

    for project in projects:
        if donation.fully_invested:
            break

        available_donate = donation.full_amount - donation.invested_amount
        project_need = project.full_amount - project.invested_amount
        min_amount = min(available_donate, project_need)

        donation.invested_amount += min_amount
        project.invested_amount += min_amount

        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.utcnow()

        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.utcnow()

        session.add(project)

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
    for donation in donations:
        if project.fully_invested:
            break

        available_project = project.full_amount - project.invested_amount
        donation_available = donation.full_amount - donation.invested_amount
        min_amount = min(available_project, donation_available)

        project.invested_amount += min_amount
        donation.invested_amount += min_amount

        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.utcnow()

        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.utcnow()

        session.add(donation)

    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project
