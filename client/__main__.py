import yaml
import json
import socket
from datetime import datetime
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration file', # help
#    required=True                       # по умолчанию False
)

args = parser.parse_args()                              # передаем введенные агрументы

# аргументы по умолчанию
host = 'localhost'
port = 8000
buffersize = 1024                                       # размер буфера сообщения в байтах
encoding = 'utf-8'                                      # кодировка

if args.config:
    with open(args.config) as file:
        config = yaml.load(file, Loader=yaml.Loader)
        host = config.get('host')
        port = config.get('port')

try:
    sock = socket.socket()                             # создаем сокет, по умолчанию tcp-сокет
    sock.connect((host, port))                         # подключаемся к серверу
    print('Client started')
    action = input('Input action: ')                   # вводим запрашиваемое дийствие
    data = input('Input your message: ')               # вводим сообщение
    request = {                                        # формируем объект запроса к серверу
        'action': action,
        'data': data,
        'time': datetime.now().timestamp()             # добавляем временную метку
    }
    s_requets = json.dumps(request)                    # формируем строковый запрос
    sock.send(s_requets.encode(encoding))                   # кодируем и отправляем сообщение
    response = sock.recv(buffersize)                   # получаем ответ
    print('Server: ', response.decode(encoding))
except KeyboardInterrupt:
    pass
