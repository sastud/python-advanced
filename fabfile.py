'''
вводится для сокращения запуска, требует установки модуля fabric3
запускаем через утилиту fab, например:
    fab server
    fab client
    fab test
'''

from fabric.api import local


def server():
    local('python server')


def client(mode='w'):
    local(f'python client -m {mode}')   # для запуска клиента в режиме read нужно запускать его
                                        # через fab client:r
                                        # либо
                                        # через python client -m r


def test():
    local('pytest --cov-report term-missing --cov server')
