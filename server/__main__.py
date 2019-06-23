import yaml
import socket
import json
import logging
import select
import threading
from argparse import ArgumentParser
from actions import resolve
from handlers import handle_default_request
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
logfile = 'server.log'

# читаем аргументы из yaml-файла, если они указаны ключом
if args.config:
    with open(args.config) as file:
        config = yaml.load(file, Loader=yaml.Loader)
        host = config.get('host')
        port = config.get('port')

'''
# создаем объект logger 'main'
logger = logging.getLogger('main')
# создаем объект форматера
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# создаем handler (файловый)
f_handler = logging.FileHandler(f'{logfile}', encoding=encoding)
# связываем компоненты между собой
f_handler.setFormatter(formatter)                           # указываем formatter для handler
f_handler.setLevel(logging.DEBUG)                           # указываем уровень логирования для handler
logger.addHandler(f_handler)                                # подключаем созданный файловый handler к logger'у
logger.addHandler(logging.StreamHandler())                  # подключаем потоковый handler к logger'у (stdout)
logger.setLevel(logging.DEBUG)                              # указываем уровень логирования для logger'а
'''
# описываем базовую конф логгера, применяется для все исп логгеров
logging.basicConfig(
    # описываем уровень лога
    level=logging.DEBUG,
    # описываем формат лога
    format='%(asctime)s - %(levelname)s - %(message)s',
    # описываем хендлеры
    handlers=[
        logging.FileHandler(f'{logfile}', encoding=encoding),
        logging.StreamHandler()
    ]
)

# формируем список пользовательских подключений
connections = []
# и запросов
requests = []


# формируем функцию чтения данных от клиента
def read(client, requests, buffersize):
    b_request = client.recv(buffersize)
    requests.append(b_request)


# формируем функцию отправки данных клиенту (всем клиентам, готовым принимать ответ сервера)
def write(client, response):
    client.send(response)


# запускаем сервер
try:
    sock = socket.socket()                                  # создаем сокет, по умолчанию tcp-сокет
    sock.bind((host, port))                                 # создаем привязку к адрес:порт
    sock.setblocking(False)                                 # делаем сервер неблокируемым так
#    sock.settimeout(0)                                     # либо так
    sock.listen(5)                                          # слушаем до 5 подключений одновременно
#    print(f'Server was started with {host}:{port}')
#    logger.info(f'Server was started with {host}:{port}')
    logging.info(f'Server was started with {host}:{port}')
    while True:
        try:
            client, address = sock.accept()                     # принимаем запрос на соединение клиента (сокет клиента)
            logging.info(f'client with address {address} detected') # логируем обнаруженное соединение
            connections.append(client)                          # добавляем клиентское подключение в списокподключений
        except:
            pass

        if connections:     # вариант обхода проблемы select в windows
            # определяем списки элементов, открытых для чтения/записи/обработки исключений
            rlist, wlist, xlist = select.select(connections, connections, connections, 0)

            # print(rlist)
            # print(wlist)

            for r_client in rlist:
                r_thread = threading.Thread(target=read, args=(r_client, requests, buffersize))      # формируем объект thread
                r_thread.start()     # запускаем потоки в цикле, тем самым получаем данные от нескольких одновременно подключенных клиентов
                # b_request = r_client.recv(buffersize)              # принято от клиента
                # requests.append(b_request)                       # добавлено в список запросов

            if requests:                                         # если запросы имеются
                b_request = requests.pop()                       # то отправляем последний из них
                b_response = handle_default_request(b_request)   # берем логику обработки запроса клиента из handlers, формируем байтовый ответ
                for w_client in wlist:
                    w_thread = threading.Thread(target=write, args=(w_client, b_response))  # формируем объект thread
                    w_thread.start()  # запускаем потоки в цикле, тем самым отправляем данные от нескольких одновременно подключенных клиентов
                    # w_client.send(b_response)                             # отправляем ответ всем клиентам, готовым принимать ответ
    #        client.close()                                      # закрываем соединение
except KeyboardInterrupt:
    pass
