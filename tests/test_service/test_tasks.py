import datetime

import pytest
import pytest_asyncio
from sqlalchemy import delete

from src.models import TaskComment
from src.models.task import Task
from src.models.user import User
from src.schemas.comment import CommentCreateSchema
from src.schemas.task import TaskCreateSchema, TaskUpdateSchema
from src.schemas.team import TeamCreateSchema
from src.services.task_service import (add_comment_to_task, create_task,
                                       delete_task, get_comments_for_task,
                                       get_task, list_all_tasks, list_tasks,
                                       update_task)
from src.services.team_service import create_team, delete_team


@pytest_asyncio.fixture
async def team(session):
    team_data = TeamCreateSchema(name="Test Team", code="TST001", users=[])
    team_obj = await create_team(session, team_data)
    yield team_obj
    await session.execute(delete(Task).where(Task.team_id == team_obj.id))
    await session.commit()
    await delete_team(session, team_obj.id)


@pytest.mark.asyncio
async def test_create_and_get_task(session, team, users):
    data = TaskCreateSchema(
        title="Test Task",
        description="Desc",
        assignee_id=users[0].id,
        deadline=datetime.datetime.now(),
        team_id=team.id,
    )
    task = await create_task(session, data)

    assert task.id is not None
    assert task.title == "Test Task"

    fetched = await get_task(session, task.id)
    assert fetched.id == task.id


@pytest.mark.asyncio
async def test_get_task_not_found_raises(session):
    with pytest.raises(Exception):
        await get_task(session, 999999)


@pytest.mark.asyncio
async def test_list_tasks_and_list_all(session, team, users):
    assignee_id = users[0].id
    await create_task(
        session,
        TaskCreateSchema(
            title="T1",
            description="d1",
            assignee_id=assignee_id,
            deadline=datetime.datetime.now(),
            team_id=team.id,
        ),
    )
    await create_task(
        session,
        TaskCreateSchema(
            title="T2",
            description="d2",
            assignee_id=assignee_id,
            deadline=datetime.datetime.now(),
            team_id=team.id,
        ),
    )
    await create_task(
        session,
        TaskCreateSchema(
            title="T3",
            description="d3",
            assignee_id=users[1].id,
            deadline=datetime.datetime.now(),
            team_id=team.id,
        ),
    )

    tasks_for_assignee = await list_tasks(session, assignee_id)
    assert len(tasks_for_assignee) == 2
    all_tasks = await list_all_tasks(session)
    assert len(all_tasks) >= 3


@pytest.mark.asyncio
async def test_update_task(session, team, users):
    data = TaskCreateSchema(
        title="Original",
        description="desc",
        assignee_id=users[0].id,
        deadline=datetime.datetime.now(),
        team_id=team.id,
    )
    task = await create_task(session, data)

    update_data = TaskUpdateSchema(
        title="Updated",
        description="desc",
        assignee_id=users[0].id,
        deadline=datetime.datetime.now(),
        team_id=team.id,
    )
    updated = await update_task(session, task.id, update_data)

    assert updated.title == "Updated"


@pytest.mark.asyncio
async def test_delete_task(session, team, users):
    data = TaskCreateSchema(
        title="ToDelete",
        description="desc",
        assignee_id=users[0].id,
        deadline=datetime.datetime.now(),
        team_id=team.id,
    )
    task = await create_task(session, data)

    result = await delete_task(session, task.id)
    assert result is True

    with pytest.raises(Exception):
        await get_task(session, task.id)


@pytest.mark.asyncio
async def test_add_comment_and_get_comments(session, team, users):
    task = await create_task(
        session,
        TaskCreateSchema(
            title="WithComment",
            description="desc",
            assignee_id=users[0].id,
            deadline=datetime.datetime.now(),
            team_id=team.id,
        ),
    )
    user_id = users[1].id
    comment_data = CommentCreateSchema(content="Hello!")

    comment = await add_comment_to_task(session, task.id, user_id, comment_data)
    assert comment.id is not None
    assert comment.content == "Hello!"

    comments = await get_comments_for_task(session, task.id)
    assert len(comments) >= 1
    assert comments[0].content == "Hello!"
