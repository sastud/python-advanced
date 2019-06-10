from functools import reduce
from settings import INSTALLED_APPS


'''
# функция сбора всех доступных действий
def get_server_actions():
    return reduce(
        # собираем все доступные actionnames
        lambda value, item: value + getattr(item, 'actionnames', []),
        reduce(
            # собираем все доступные actions
            lambda value, item: value + [getattr(item, 'actions', [])],
            reduce(
                # собираем все доступные модули (echo, messenger, etc)
                lambda value, item: value + [__import__(f'{item}.actions')],
                INSTALLED_APPS,
                []  # значение по умолчанию, если ничего нет
            ),
            []  # значение по умолчанию, если ничего нет
        ),
        []  # значение по умолчанию, если ничего нет
    )
'''


# функция сбора всех доступных действий (традиционный вид)
def get_server_actions():
    modules = reduce(
        # собираем все доступные модули (echo, messenger, etc)
        lambda value, item: value + [__import__(f'{item}.actions')],
        INSTALLED_APPS,
        []  # значение по умолчанию, если ничего нет
    )
    actions = reduce(
        # собираем все доступные actions
        lambda value, item: value + [getattr(item, 'actions', [])],
        modules,
        []  # значение по умолчанию, если ничего нет
    )
    actionnames = reduce(
        # собираем все доступные actionnames
        lambda value, item: value + getattr(item, 'actionnames', []),
        actions,
        []  # значение по умолчанию, если ничего нет
    )
    return actionnames


# функция резолва конкретного действия из общего собранного списка
def resolve(action_name, actions=None):
    actions_list = actions or get_server_actions()
    actions_mapping = {
        action.get('action'): action.get('controller')
        for action in actions_list
    }
    return actions_mapping.get(action_name)

