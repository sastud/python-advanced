# тест функции get_echo() из controllers.py эхо-сервера

from datetime import datetime
from echo.controllers import get_echo       # импортируем функцию get_echo(), чтобы проверить ее
import pytest                               # импортируем для создания фикстур


# описываем фикстуры (как декораторы), чтобы не дублировать часть кода
# затем используем фикстуры в функциях тестов, обращаясь к ним как к аргументам

@pytest.fixture
def action_fixture():
    return 'echo'


@pytest.fixture
def time_fixture():
    return datetime.now().timestamp()


@pytest.fixture
def data_fixture():
    return 'data'


# объект запроса
@pytest.fixture
def request_fixture(action_fixture, time_fixture, data_fixture):
    return {
        'action': action_fixture,
        'time': time_fixture,
        'data': data_fixture
    }


# ожидаемый ответ сервера
@pytest.fixture
def expected_fixture(action_fixture, time_fixture, data_fixture):
    return {
        'action': action_fixture,
        'user': None,
        'time': time_fixture,
        'data': data_fixture,
        'code': 200
    }


def test_get_echo(request_fixture, expected_fixture):
    # фактический ответ сервера
    response = get_echo(request_fixture)

    # тестирование - сравниваем результаты по элементам словаря
    # запускаем pytest из корня программы "server" (либо "client", если для него написаны тесты)
    assert expected_fixture.get('code') == response.get('code')
