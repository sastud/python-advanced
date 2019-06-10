from protocol import make_response

# функция эхо-сервера
def get_echo(request):
    data = request.get('data')
    return make_response(
        request, 200, data      # ответ сервера с кодом успеха
    )
