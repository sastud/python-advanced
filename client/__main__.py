import yaml
import json
import socket
import hashlib
import zlib
import threading
from datetime import datetime
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration file', # help
#    required=True                       # по умолчанию False
)

# описываем вариант запуска клиента в режиме записи
parser.add_argument(
    '-m', '--mode', type=str, default='w',
    help='Sets client mode'
)

args = parser.parse_args()                              # передаем введенные агрументы

# аргументы по умолчанию
host = 'localhost'
port = 8000
buffersize = 1024                                       # размер буфера сообщения в байтах
encoding = 'utf-8'                                      # кодировка


def read():
    response = sock.recv(buffersize)  # получаем ответ
    b_response = zlib.decompress(response)             # распаковываем ответ сервера
    print('Server: ', b_response.decode(encoding))     # выводим декодированный ответ сервера


def write():
    while True:  # бесконечный цикл
        hash_obj = hashlib.sha256()  # формируем объект с хешем, чтобы передать его в поле user запроса к серверу
        hash_obj.update(str(datetime.now().timestamp()).encode(encoding))  # обновляем "солью" в виде текущей timestamp и кодируем в байтовую последовательность
        action = input('Input action: ')                   # вводим запрашиваемое действие
        data = input('Input your message: ')               # вводим сообщение
        request = {                                        # формируем объект запроса к серверу
            'action': action,
            'data': data,
            'time': datetime.now().timestamp(),            # добавляем временную метку
            'user': hash_obj.hexdigest()                   # формируем 16-ричное представление объекта hash_obj. без него получим 403 от сервера
        }
        s_request = json.dumps(request)                    # формируем строковый запрос
        b_request = zlib.compress(s_request.encode(encoding))   # формируем сжатый байтовый запрос
        sock.send(b_request)                               # отправляем сжатое сообщение


if args.config:
    with open(args.config) as file:
        config = yaml.load(file, Loader=yaml.Loader)
        host = config.get('host')
        port = config.get('port')

try:
    sock = socket.socket()                             # создаем сокет, по умолчанию tcp-сокет
    sock.connect((host, port))                         # подключаемся к серверу
    print('Client started')

    if args.mode == 'w':                                # если клиент запущен в режиме отправки сообщений
        write()
        # while True:                                    # бесконечный цикл
        #     hash_obj = hashlib.sha256()  # формируем объект с хешем, чтобы передать его в поле user запроса к серверу
        #     hash_obj.update(str(datetime.now().timestamp()).encode(encoding))  # обновляем "солью" в виде текущей timestamp и кодируем в байтовую последовательность
        #     action = input('Input action: ')                   # вводим запрашиваемое действие
        #     data = input('Input your message: ')               # вводим сообщение
        #     request = {                                        # формируем объект запроса к серверу
        #         'action': action,
        #         'data': data,
        #         'time': datetime.now().timestamp(),            # добавляем временную метку
        #         'user': hash_obj.hexdigest()                   # формируем 16-ричное представление объекта hash_obj. без него получим 403 от сервера
        #     }
        #     s_request = json.dumps(request)                    # формируем строковый запрос
        #     b_request = zlib.compress(s_request.encode(encoding))   # формируем сжатый байтовый запрос
        #     sock.send(b_request)                               # отправляем сжатое сообщение
    elif args.mode == 'wr':
        # формируем объект thread, позволяющий парраллельно читать данные из основного потока
        r_thread = threading.Thread(target=read, daemon=True)  # daemon нужен для запуска потока в фоновом режиме параллельно с основным потоком программы
        r_thread.start()    # запускаем
        write()
    else:                                              # если клиент запущен в режиме чтения
        read()
        # while True:                                            # бесконечный цикл
            # response = sock.recv(buffersize)                   # получаем ответ
            # b_response = zlib.decompress(response)             # распаковываем ответ сервера
            # print('Server: ', b_response.decode(encoding))     # выводим декодированный ответ сервера
except KeyboardInterrupt:
    pass
