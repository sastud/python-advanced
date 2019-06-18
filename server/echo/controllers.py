from protocol import make_response
# импортируем декораторы logger_required и login_required
from decorators import (
    logger_required,
    login_required
)

# функция эхо-сервера
@login_required     # декорируем функцию эхо-сервера докоратором проверки логина
@logger_required    # декорируем функцию эхо-сервера докоратором логирования
def get_echo(request):
    data = request.get('data')
    return make_response(
        request, 200, data      # ответ сервера с кодом успеха
    )
