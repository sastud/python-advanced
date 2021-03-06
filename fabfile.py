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


def client():
    local('python client')


def test():
    local('pytest --cov-report term-missing --cov server')
