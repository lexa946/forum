import pytest
from httpx import AsyncClient

@pytest.mark.parametrize("title,text,nick,status_code",[
    ("Еще один тредик", "А вот тут я хочу поделится секретом", "Анон228", 200),
    ("", "Тред с пустым заголовком", "Анон", 422),
    (None, "Тред без заголовка", "Анон", 422),
    ("Тред без описания", None, "Анон", 422),
    ("Тред c пустым описанием", "", "Анон", 422),
    ("Тредик", "Тред без ника совсем", None, 200),
    ("Тредик", "Тред с пустым ником", "", 200),
    (None, None, None, 422),
])
async def test_add_thread(title, text, nick, status_code, ac: AsyncClient):
    response = await ac.post('/forum/api/v1/thread/', json={
        "title": title,
        "text": text,
        "nick": nick
    })
    print(response.text)
    assert response.status_code == status_code
    if not response.is_success:
        return

    thread = response.json()['thread']

    assert thread['title'] == title
    assert thread['text'] == text

    print(thread['nick'])
    if nick:
        assert thread['nick'] == nick

    else:
        assert thread['nick'] == "Аноним"



@pytest.mark.parametrize('thread_id,title,text,nick,status_code', [
    (1,"Мой первый тредик", "Тут мы будем обсуждать все хорошее, а плохое не будем", "Алёша", 200),
    (2,"Обмен файлами", "Реквестую видео где смеется обезьяна", "ТвояБабка", 200),
    (200,None, None, None, 404),

])
async def test_get_thread(thread_id, title, text, nick, status_code,ac: AsyncClient):
    response = await ac.get(f'/forum/api/v1/thread/{thread_id}')
    assert response.status_code == status_code
    if not response.is_success: return


    thread = response.json()['thread']
    assert thread.get('id') == thread_id
    assert thread.get('title') == title
    assert thread.get('text') == text
    assert thread.get('nick') == nick
