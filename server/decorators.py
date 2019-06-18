import logging
from functools import wraps
from protocol import make_response


# создаем объект логгера
logger = logging.getLogger('decorators')


# описываем декоратор логирования
def logger_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger.debug(f'{func.__name__}: {request}')
        return func(request, *args, **kwargs)
    return wrapper


# описываем декоратор идентификации пользователя на основе хеша сессии
# пользователь без без этого поля данных (аноним) не сможет обращаться к имеющимся модулям сервера
def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'user' in request:
            # если поле user присутствует в запросе пользователя, то запрос обрабатывается
            return func(request, *args, **kwargs)
        # иначе передаем 403 и сообщение 'access denied'
        return make_response(request, 403, 'access denied!')
    return wrapper
