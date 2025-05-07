from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB
)
from app.api.validators import (
    check_name_duplicate, check_exist_project,
    check_before_delete_invested_amount,
    check_close_date,
    check_invested_amount_valid
)
from app.services.process_invest import investment_project


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    summary='Возвращает список всех проектов'
)
async def get_all_project(
    session: AsyncSession = Depends(get_async_session)
):
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создает проект'
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    new_project = await investment_project(project=new_project, session=session)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Редактирует проект'
)
async def update_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    project = await check_exist_project(project_id, session)
    if project_in.name is not None:
        await check_name_duplicate(project_in.name, session)
    if project.fully_invested:
        await check_close_date(project)
    if project_in.full_amount is not None:
        await check_invested_amount_valid(project, project_in.full_amount)

    project = await charity_project_crud.update(
        project, project_in, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Удаляет проект'
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    project = await check_exist_project(project_id, session)
    await check_before_delete_invested_amount(project)
    project = await charity_project_crud.remove(project, session)
    return project
