import os.path
from pathlib import Path

import pytest
from httpx import AsyncClient

from app.s3.client import s3_client


@pytest.mark.parametrize("comment_id,thread_id,text,nick,files_count,status_code", [
    (1, 1, "Да, прикольно ты сделал", "Аноним", 0, 200),
    (2, 2,"Коммент с 1 файлом", "Аноним", 1, 200),
    (3, 2,"Вот это видео?", "Санечек", 1, 200),
    (4, None, None, None, None, 404)
])
async def test_get_comment(comment_id, thread_id, text, nick, files_count, status_code, ac: AsyncClient):
    response = await ac.get(f"/forum/api/v1/comment/{comment_id}")
    assert response.status_code == status_code
    if not response.is_success: return

    comment = response.json()['comment']

    assert comment['id'] == comment_id
    assert comment['thread_id'] == thread_id
    assert comment['text'] == text
    assert comment['nick'] == nick
    assert len(comment['media']) == files_count


@pytest.mark.parametrize("thread_id,text,nick,files,status_code", [
    (1, "", "Аноним", [], 422),
    (1, "Добавление коммента", "Аноним", [], 200),
    (1, "Добавление коммента без ника", None, [], 200),
    (1, "Добавление коммента с пустым ником", "", [], 200),
    (2,"Коммент с 1 файлом новый", "Аноним", ["app/tests/test_files/test_video_small.mp4"], 200),
    (2,"Коммент с несколькими файлами", "Санечек", ["app/tests/test_files/test_video_small.mp4",
                                          "app/tests/test_files/test_video_large.mp4"], 200),


    (4, None, None, [], 422),
    (40, "Коммент в несуществующий тред", None, [], 404),
])
async def test_add_comment(thread_id, text, nick, files, status_code, ac: AsyncClient):

    files_to_send = []
    for file in files:
        file_path = Path(file)
        files_to_send.append(
            ('files', file_path.open('rb'))
        )


    response = await ac.post(f"/forum/api/v1/comment",data={
        "thread_id": thread_id,
        "text": text,
        "nick": nick,
    }, follow_redirects=True, files=files_to_send)
    assert response.status_code == status_code
    if not response.is_success: return

    comment = response.json()['comment']
    assert comment['thread_id'] == thread_id
    assert comment['text'] == text
    if nick:
        assert comment['nick'] == nick

    else:
        assert comment['nick'] == "Аноним"
    assert len(comment['media']) == len(files)
    for media_in, media_out in zip(files, comment['media']):
        assert media_out['filename'] in media_in

        s3_response = await s3_client.get_file(f"{media_out['id']}_{media_out['filename']}")
        assert s3_response['ResponseMetadata']['HTTPStatusCode'] == 200

