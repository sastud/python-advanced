import yaml
import socket
import json
import logging
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


# запускаем сервер
try:
    sock = socket.socket()                                  # создаем сокет, по умолчанию tcp-сокет
    sock.bind((host, port))                                 # создаем привязку к адрес:порт
    sock.listen(5)                                          # слушаем до 5 подключений одновременно
#    print(f'Server was started with {host}:{port}')
#    logger.info(f'Server was started with {host}:{port}')
    logging.info(f'Server was started with {host}:{port}')
    while True:
        client, address = sock.accept()                     # принимаем запрос на соединение клиента (сокет клиента)
        b_request = client.recv(buffersize)                 # принято от клиента
        b_response = handle_default_request(b_request)      # берем логику обработки запроса клиента из handlers, формируем байтовый ответ
        client.send(b_response)                             # отправляем ответ
        client.close()                                      # закрываем соединение
except KeyboardInterrupt:
    pass
