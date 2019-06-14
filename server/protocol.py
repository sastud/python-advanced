from datetime import datetime


# функция проверки клиентского запроса
def validate_request(raw):
    # обязательные параметры в запросе клиента
    if 'time' in raw and 'action' in raw:
        return True
    else:
        return False


# функция формирования ответа сервера
def make_response(request, code, data=None):
    return {
        'action': request.get('action'),
        'user': request.get('user'),
        'time': datetime.now().timestamp(), # метка текущей даты
        'data': data,
        'code': code
    }
