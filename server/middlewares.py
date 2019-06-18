# модуль с промежуточным функционалом,
# который подключается к обработчику пользовательских запросов с помощью декорирования

import zlib


# функционал работы со сжатыми данными
def compressed_middleware(func):
    def wrapper(request, *args, **kwargs):
        b_request = zlib.decompress(request)            # декомпрессия сырого сжатого запроса пользователя
        b_response = func(b_request, *args, **kwargs)   # формируем байтовый ответ сервера
        return zlib.compress(b_response)                # возвращаем сжатый ответ сервера
    return wrapper
