from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    project = await charity_project_crud.get_project_by_id_name(
        project_name, session)
    if project is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_exist_project(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


async def check_close_date(project: CharityProject) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_invested_amount_valid(
        project: CharityProject, new_full_amount: int
        ) -> None:
    if project.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=422,
            detail='Нельзя установить требуемую сумму меньше уже вложенной.'
        )


async def check_before_delete_invested_amount(project: CharityProject) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail=(
                'Нельзя удалить проект, в который уже были инвестированы'
                'средства, его можно только закрыть.'
            )
        )
