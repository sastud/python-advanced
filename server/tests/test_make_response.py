import pytest
from datetime import datetime
from protocol import make_response      # импортируем make_response(), чтобы протестировать ее


# описываем фикстуры
@pytest.fixture
def action_fixture():
    return 'action'


@pytest.fixture
def time_fixture():
    return datetime.now().timestamp()


@pytest.fixture
def data_fixture():
    return 'data'


@pytest.fixture
def code_fixture():
    return 200


# описываем корректный запрос
@pytest.fixture
def valid_request_fixture(action_fixture, time_fixture, data_fixture):
    return {
        'action': action_fixture,
        'user': None,
        'time': time_fixture,
        'data': data_fixture
    }


# описываем некорректный запрос
@pytest.fixture
def invalid_request():
    return {}       # пустой словарь будет примером некорректного запроса


# описываем тесты
def test_valid_make_response(valid_request_fixture, code_fixture):
    response = make_response(valid_request_fixture, code_fixture)
    assert response.get('code') == code_fixture
