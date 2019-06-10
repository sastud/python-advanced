import yaml
import socket
import json
from argparse import ArgumentParser
from actions import resolve
from protocol import (
    validate_request, make_response
)


# парсер аргументов
parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration file',                     # help
#    required=True                                           # по умолчанию False
)

args = parser.parse_args()                                  # передаем введенные агрументы

# аргументы по умолчанию
host = '0.0.0.0'
port = 8000
buffersize = 1024                                           # размер буфера сообщения в байтах
encoding = 'utf-8'                                          # кодировка

# читаем аргументы из yaml-файла, если они указаны ключом
if args.config:
    with open(args.config) as file:
        config = yaml.load(file, Loader=yaml.Loader)
        host = config.get('host')
        port = config.get('port')

# запускаем сервер
try:
    sock = socket.socket()                                  # создаем сокет, по умолчанию tcp-сокет
    sock.bind((host, port))                                 # создаем привязку к адрес:порт
    sock.listen(5)                                          # слушаем до 5 подключений одновременно
    print(f'Server was started with {host}:{port}')
    while True:
        client, address = sock.accept()                     # принимаем запрос на соединение клиента (сокет клиента)
        b_request = client.recv(buffersize)                 # принято от клиента
        request = json.loads(b_request.decode(encoding))    # декодируем клиентский запрос
        if validate_request(request):
            action_name = request.get('action')             # разбор запроса клиента
            controller = resolve(action_name)               # по запросу клиента находим нужный контроллер
            if controller:                                  # проверка наличия на сервере запрошенного контроллера
                try:
                    response = controller(request)          # формируем объект ответа сервера
                except Exception as err:
                    print(err)
                    response = make_response (request, 500, 'internal server error')    # обработчик ошибки сервера
            else:
                response = make_response(request, 404, 'action not found')  # действие при отсутствии нужного контроллера
        else:
            response = make_response(request, 400, 'wrong request')    # действие при некорректном запросе клиента
        s_response = json.dumps(response)                   # преобразуем обхект ответа сервера в json
        client.send(s_response.encode(encoding))            # отправляем ответ
        client.close()                                      # закрываем соединение
except KeyboardInterrupt:
    pass
