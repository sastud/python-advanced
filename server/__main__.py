import yaml
import socket
from argparse import ArgumentParser

# парсер аргументов
parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration file',     # help
#    required=True                           # по умолчанию False
)

args = parser.parse_args()                  # передаем введенные агрументы

# аргументы по умолчанию
host = '0.0.0.0'
port = 8000
buffersize = 1024               # размер буфера сообщения в байтах
encoding = 'utf-8'

# читаем аргументы из yaml-файла, если они указаны ключом
if args.config:
    with open(args.config) as file:
        config = yaml.load(file, Loader=yaml.Loader)
        host = config.get('host')
        port = config.get('port')

# запускаем сервер
try:
    sock = socket.socket()                  # создаем сокет, по умолчанию tcp-сокет
    sock.bind((host, port))                 # создаем привязку к адрес:порт
    sock.listen(5)                          # слушаем до 5 подключений одновременно
    print(f'Server was started with {host}:{port}')
    while True:
        client, address = sock.accept()     # принимаем запрос на соединение клиента (сокет клиента)
        print(f'Client was detected on {address}')
        data = client.recv(buffersize)      # получаем сообщение клиента
        print('Client message: ', data.decode(encoding))
        client.send(data)                   # отправляем ответ
        client.close()                      # закрываем соединение
except KeyboardInterrupt:
    pass
