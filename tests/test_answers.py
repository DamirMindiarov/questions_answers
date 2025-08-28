import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_add_answer_to_question(async_client, get_new_question):
    question = get_new_question

    response = await async_client.post(
        f"http://localhost:8000/questions/{question.id}/answers/",
        json={"text": "answer text"},
    )

    answer = {
        "id": response.json()["id"],
        "question_id": response.json()["question_id"],
        "user_id": response.json()["user_id"],
        "text": response.json()["text"],
        "created_at": response.json()["created_at"],
    }

    assert response.status_code == 201
    assert response.json() == answer


@pytest.mark.asyncio(loop_scope="session")
async def test_get_answer_by_id(
    async_client, get_new_question, get_question_response
):
    question = get_new_question
    response = await async_client.get(
        f"http://localhost:8000/answers/{question.answer[0].id}"
    )

    assert response.status_code == 200
    assert response.json() in get_question_response["answer"]


@pytest.mark.asyncio(loop_scope="session")
async def test_del_answer_by_id(async_client, get_new_question):
    question = get_new_question

    added_answer = await async_client.post(
        f"http://localhost:8000/questions/{question.id}/answers/",
        json={"text": "answer text"},
    )
    response = await async_client.delete(
        f"http://localhost:8000/answers/{added_answer.json()["id"]}"
    )

    assert response.status_code == 200
    assert (
        response.json() == f"deleted answer with id {added_answer.json()["id"]}"
    )
