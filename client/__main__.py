import yaml
import socket
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration file', # help
#    required=True                       # по умолчанию False
)

args = parser.parse_args()              # передаем введенные агрументы

# аргументы по умолчанию
host = 'localhost'
port = 8000
buffersize = 1024                       # размер буфера сообщения в байтах
encoding = 'utf-8'

if args.config:
    with open(args.config) as file:
        config = yaml.load(file, Loader=yaml.Loader)
        host = config.get('host')
        port = config.get('port')

try:
    sock = socket.socket()              # создаем сокет, по умолчанию tcp-сокет
    sock.connect((host, port))          # подключаемся к серверу
    print('Client started')
    data = input('You: ')               # вводим сообщение
    sock.send(data.encode(encoding))    # кодируем и отправляем сообщение
    response = sock.recv(buffersize)    # получаем ответ
    print('Server: ', response.decode(encoding))
    # while True:
    #     data = input('You: ')
    #     sock.send(data.encode(encoding))
    #     response = sock.recv(buffersize)
    #     print('Server: ', response.decode(encoding))
except KeyboardInterrupt:
    pass
