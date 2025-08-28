import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_create_new_question(async_client):
    response = await async_client.post(
        f"http://localhost:8000/questions/", json={"text": "new text"}
    )

    assert response.status_code == 201
    assert response.json()["text"] == "new text"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_list_all_questions(async_client, get_new_question, get_session, get_question_response):
    response = await async_client.get(
        f"http://localhost:8000/questions/"
    )

    assert response.status_code == 200
    assert get_question_response in response.json()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_question_by_id(async_client, get_new_question, get_session, get_question_response):
    question = get_new_question
    response = await async_client.get(
        f"http://localhost:8000/questions/{question.id}"
    )

    assert response.status_code == 200
    assert response.json() == get_question_response


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_question_by_id(async_client, get_new_question):
    question = get_new_question
    response = await async_client.delete(
        f"http://localhost:8000/questions/{question.id}"
    )

    assert response.status_code == 200
    assert response.json() == f'deleted question with id {question.id}'
