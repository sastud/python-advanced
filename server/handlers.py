# выделенный обработчик пользовательского запроса
import json
import logging
from actions import resolve
from protocol import (
    validate_request, make_response
)
from middlewares import compressed_middleware

# обработчик стандартного запроса (просто сырую байтовую строку)
@compressed_middleware      # декорирован доп.функционалом работы со сжатыми данными
def handle_default_request(raw_request):
    request = json.loads(raw_request.decode())
    if validate_request(request):
        action_name = request.get('action')  # разбор запроса клиента
        controller = resolve(action_name)  # по запросу клиента находим нужный контроллер
        if controller:  # проверка наличия на сервере запрошенного контроллера
            try:
                response = controller(request)  # формируем объект ответа сервера
            except Exception as err:
#                    print(err)
#                    logger.critical(err)   # логирование критической ошибки сервера (вызвавшей исключение и падение сервера)
                logging.critical(err)  # аналогично, объекта логгера будет создан автоматически самим модулем logging
                response = make_response(request, 500, 'internal server error')  # обработчик ошибки сервера
        else:
#                logger.error(f'404 - request: {request}')   # логирование ошибки сервера с указанием request, вызвавшего ее
            logging.error(
                f'404 - request: {request}')  # аналогично, объекта логгера будет создан автоматически самим модулем logging
            response = make_response(request, 404, 'action not found')  # действие при отсутствии нужного контроллера
    else:
#            logger.error(f'400 - request: {request}')  # логирование ошибки сервера с указанием request, вызвавшего ее
        logging.error(
            f'400 - request: {request}')  # аналогично, объекта логгера будет создан автоматически самим модулем logging
        response = make_response(request, 400, 'wrong request')  # действие при некорректном запросе клиента

    # ответ клиенту в json
    return json.dumps(response).encode()
