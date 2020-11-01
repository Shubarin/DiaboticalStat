# coding=utf-8
import argparse
import time

import requests

import my_exceptions


def is_valid(mode, country):
    """Проверяет корректность введенных параметров.
    Parameters:
        args (dict): словарь, содержащий все аргументы и их значения,
    полученные из командной строки
    Returns:
        True/False (bool): результат проверки на корректность.
    """
    # Список возможных значений аргумента mode
    modes = [
        'r_macguffin',
        'r_wo',
        'r_rocket_arena_2',
        'r_shaft_arena_1',
        'r_ca_2',
        'r_ca_1'
    ]
    # Список возможных значений аргумента country по ISO
    countries = [
        'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao', 'aq', 'ar',
        'as', 'at', 'au', 'aw', 'az', 'bb', 'bd', 'be', 'bf', 'bg', 'bh',
        'bi', 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bv', 'bw', 'by',
        'bz', 'ca', 'cc', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn',
        'co', 'cr', 'cu', 'cv', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm',
        'do', 'dz', 'ec', 'ee', 'eg', 'eh', 'es', 'et', 'fi', 'fj', 'fk',
        'fm', 'fo', 'fr', 'ga', 'gb', 'gd', 'ge', 'gf', 'gh', 'gi', 'gl',
        'gm', 'gn', 'gp', 'gq', 'gr', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm',
        'hn', 'ht', 'hu', 'id', 'ie', 'il', 'im', 'in', 'io', 'iq', 'ir',
        'is', 'it', 'jm', 'jo', 'jp', 'jt', 'ke', 'kg', 'kh', 'ki', 'km',
        'kn', 'kp', 'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk',
        'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'mg', 'mh',
        'mi', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu',
        'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nc', 'ne', 'nf', 'ng', 'ni',
        'nl', 'no', 'np', 'nr', 'nt', 'nu', 'nz', 'om', 'pa', 'pe', 'pf',
        'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'pr', 'pt', 'pw', 'py', 'qa',
        're', 'ro', 'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh',
        'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'sv', 'sy', 'sz',
        'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tm', 'tn', 'to', 'tp',
        'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 'um', 'us', 'uy', 'uz',
        'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'wk', 'ws', 'ye',
        'yu', 'za', 'zm', 'zr', 'zw', ''
    ]
    if mode not in modes:
        raise my_exceptions.ModeError('Неверное значение аргумента --mode')

    if country is not None and country.lower() not in countries:
        raise my_exceptions.CountryError('неверное значение '
                                         'аргумента --country')

    return True


def delete_user_id_field(old_data):
    """Удаляет из словаря пару ключ 'user_id'.
    Parameters:
        old_data (list): список словарей, содержащий все
    записи, полученные из запроса
    """
    for user in old_data:
        del user['user_id']


def request_response(params):
    """Выполняет запрос к api_server.
        Parameters:
            params (dict): словарь, параметров запроса
        Returns response (requests.models.Response): ответ от api_server
    """
    api_server = 'https://www.diabotical.com/api/v0/stats/leaderboard'
    try:
        return requests.get(api_server, params=params)
    except:
        raise my_exceptions.UnavailableServer('ошибка сервера')


def get_result(count, user_id, country, json_response):
    """Выполняет подготовку данных для вывода.
    Parameters:
        count (int): количество записей в выборке;
        user_id (str): user_id пользователя, для которого выполняется запрос;
        country (str): страна, для которой выполняется запрос;
        json_response (dict): словарь, содержащий все аргументы и
    их значения, полученные из командной строки
    Returns:
        result (dict): словарь с результатами выполнения запроса;
        result (int): число записей удовлетворяющих условиям запроса.
    """
    result = json_response.get('leaderboard', '')[:count]

    if user_id is not None:
        result = get_info_for_user_id(result, user_id)

    if country is not None:
        result = get_info_for_country(result, country)

    if isinstance(result, list):
        if result:
            delete_user_id_field(result)
        result = {'leaderboard': result}

    return result


def get_info_for_user_id(data, user_id):
    """Получает информацию о пользователе из результатов запроса.
        Parameters:
            data (list): список словарей, содержащий все
    записи, полученные из запроса
            user_id (str): значение user_id, запрошенного пользователя
        Returns:
            result (list): список сведений о пользователе.
    """
    result = [user for user in data if user['user_id'] == user_id]
    return result


def get_info_for_country(data, country):
    """Получает информацию о пользователе из результатов запроса.
        Parameters:
            data (list): список словарей, содержащий все
    записи, полученные из запроса
            country (str): значение country, запрошенной страны
        Returns:
            country_count (int): количество игроков заданной страны.
    """
    country_count = sum([1 if user['country'] == country else 0
                         for user in data])
    return country_count


def parse_command_line():
    """Создает аргументы для выполнения скрипта в командной строке.
    Разделяет команду на ключи и параметры.

    Returns:
        args (Namespace): список полученных параметров.
    """
    parser = argparse.ArgumentParser(description='reading player statistics '
                                                 'in Diabotic via the API')

    parser.add_argument('mode', type=str, help='string line')
    parser.add_argument('--mode', action='store_const', const=sum,
                        help='Available values : r_macguffin, r_wo, '
                             'r_rocket_arena_2, r_shaft_arena_1,'
                             ' r_ca_2, r_ca_1')

    parser.add_argument('--count', default=None, type=int,
                        help='The count argument is optional. '
                             'By default, it is equal to the '
                             'number of records returned by '
                             'the API')

    parser.add_argument('--user_id', default=None, type=str,
                        help='Find and display information about a '
                             'player with a specific user_id')

    parser.add_argument('--country', default=None, type=str,
                        help='Count the number of players in a '
                             'particular country')

    args = parser.parse_args()
    return args


def main():
    """Основная функция. Запускается при запуске файла в командной строке
    Returns:
        result (str): сообщение с результатом выполнения программы.
    """
    try:
        context = vars(parse_command_line())  # приводим тип Namespace к dict
        mode = context['mode']
        count = context['count']
        user_id = context['user_id']
        country = context['country']
        lines_per_page = 20  # максимальное количество результатов на странице
        max_count = 500  # максимум результатов, хранящихся в таблице

        if count is None:
            count = lines_per_page

        count = min(max_count, count)

        result = 'Error in arguments'
        if is_valid(mode, country):
            offset = 0
            params = {
                'mode': mode,
                'offset': 0
            }
            # Считаем количество запросов к api в зависимости от count
            n = (count + lines_per_page - 1) // lines_per_page
            for _ in range(n):
                params['offset'] = offset
                response = request_response(params)
                json_response = response.json()
                current_result = get_result(count, user_id,
                                            country, json_response)
                if (isinstance(result, str) and
                        isinstance(current_result, int)):
                    result = 0
                elif (isinstance(result, str) and
                      isinstance(current_result, dict)):
                    result = {'leaderboard': []}

                if isinstance(current_result, int):
                    result += current_result
                else:
                    result['leaderboard'].extend(
                        current_result['leaderboard']
                    )
                offset += lines_per_page
                count -= lines_per_page
                time.sleep(0.2)
    except Exception as e:
        result = e

    print(result)
    exit(code=0)


if __name__ == '__main__':
    main()
