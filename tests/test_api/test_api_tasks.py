import datetime

import pytest


@pytest.mark.asyncio
async def test_create_task(
    session, client, override_require_role_admin, mock_user, override_current_user
):
    data = {
        "title": "Test task",
        "description": "Check if task creation works",
        "assignee_id": str(mock_user.id),
        "deadline": str(datetime.datetime.now()),
        "team_id": str(mock_user.team_id),
    }

    response = await client.post("/tasks/", json=data)
    assert response.status_code == 200
    resp = response.json()
    assert resp["title"] == data["title"]
    assert resp["description"] == data["description"]


@pytest.mark.asyncio
async def test_get_task_by_id(
    session, client, override_require_role_admin, mock_user, override_current_user
):
    data = {
        "title": "Task to retrieve",
        "description": "Retrieval test",
        "assignee_id": str(mock_user.id),
        "deadline": str(datetime.datetime.now()),
        "team_id": str(mock_user.team_id),
    }
    created = await client.post("/tasks/", json=data)
    print(created.json())
    task_id = created.json()["id"]

    response = await client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_update_task(
    session, client, override_require_role_admin, mock_user, override_current_user
):
    data = {
        "title": "Original title",
        "description": "To be updated",
        "assignee_id": str(mock_user.id),
        "deadline": str(datetime.datetime.now()),
        "team_id": str(mock_user.team_id),
    }
    created = await client.post("/tasks/", json=data)
    task_id = created.json()["id"]

    update_data = {"title": "Updated title"}
    updated = await client.put(f"/tasks/{task_id}", json=update_data)
    assert updated.status_code == 200
    assert updated.json()["title"] == "Updated title"


@pytest.mark.asyncio
async def test_delete_task(
    session, client, override_require_role_admin, mock_user, override_current_user
):
    data = {
        "title": "Task to delete",
        "description": "Will be deleted",
        "assignee_id": str(mock_user.id),
        "deadline": str(datetime.datetime.now()),
        "team_id": str(mock_user.team_id),
    }
    created = await client.post("/tasks/", json=data)
    task_id = created.json()["id"]
    print(task_id)

    deleted = await client.delete(f"/tasks/{task_id}")
    assert deleted.status_code == 200
    assert deleted.json()["status"] == "deleted"

    get_after_delete = await client.get(f"/tasks/{task_id}")
    assert get_after_delete.status_code == 404


@pytest.mark.asyncio
async def test_add_comment_to_task(session, client, mock_user, override_current_user):
    data = {
        "title": "Task with comment",
        "description": "To receive a comment",
        "assignee_id": str(mock_user.id),
        "deadline": str(datetime.datetime.now()),
        "team_id": str(mock_user.team_id),
    }
    created = await client.post("/tasks/", json=data)
    task_id = created.json()["id"]

    comment = {"content": "This is a test comment"}
    response = await client.post(f"/tasks/{task_id}/comments", json=comment)
    assert response.status_code == 200
    assert response.json()["content"] == comment["content"]
    assert response.json()["user_id"] == str(mock_user.id)


@pytest.mark.asyncio
async def test_get_task_comments(session, client, mock_user, override_current_user):
    data = {
        "title": "Task for comment reading",
        "description": "Testing comment list",
        "assignee_id": str(mock_user.id),
        "deadline": str(datetime.datetime.now()),
        "team_id": str(mock_user.team_id),
    }
    created = await client.post("/tasks/", json=data)
    task_id = created.json()["id"]

    comment = {"content": "Another comment"}
    await client.post(f"/tasks/{task_id}/comments", json=comment)

    response = await client.get(f"/tasks/{task_id}/comments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(c["content"] == "Another comment" for c in response.json())
