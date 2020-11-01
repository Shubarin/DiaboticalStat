import time

import leaderboard
from my_exceptions import ParametersException, ConnectException


def test_main():
    test_data = [
        ({'mode': 'r_macguffin',
          'count': 3,
          'user_id': None,
          'country': None}, 3),
        ({'mode': 'r_macguffin',
          'count': 21,
          'user_id': None,
          'country': None}, 21),
        ({'mode': 'r_macguffin',
          'count': 500,
          'user_id': None,
          'country': None}, 500),
        ({'mode': 'r_macguffin',
          'count': None,
          'user_id': None,
          'country': None}, 20),
        ({'mode': 'r_macguffin',
          'count': None,
          'user_id': 123,
          'country': None}, 0),
        ({'mode': 'r_macguffin',
          'count': 100,
          'user_id': 'a561674a91274f878ea610c66bb278e0',
          'country': None}, 1),
        ({'mode': 'r_macguffin',
          'count': 2,
          'user_id': 'a561674a91274f878ea610c66bb278e0',
          'country': None}, 0),
        ({'mode': 'r_macguffin',
          'count': 500,
          'user_id': '6efb90feac604cbe9db1a5282b16c604',
          'country': None}, 1),
        ({'mode': 'r_macguffin',
          'count': None,
          'user_id': '6efb90feac604cbe9db1a5282b16c604',
          'country': None}, 0),
        ({'mode': 'r_macguffin',
          'count': 500,
          'user_id': None,
          'country': 'ru'}, 28),
        ({'mode': 'r_macguffin',
          'count': 500,
          'user_id': None,
          'country': ''}, 100),
        ({'mode': 'r_macguffin',
          'count': None,
          'user_id': '6efb90feac604cbe9db1a5282b16c604',
          'country': 'tr'}, 1),

    ]
    for i, (request, correct_output) in enumerate(test_data, 1):
        try:
            test_result = leaderboard.main(request)
            if isinstance(test_result, int):
                assert test_result <= correct_output, \
                    f'Номер теста {i}, {test_result} != {correct_output}'
            else:
                assert len(test_result['leaderboard']) == correct_output, \
                    f'Номер теста {i}, ' \
                        f'{len(test_result["leaderboard"])} != {correct_output}'
        except ParametersException:
            continue
        except ConnectException:
            continue
        except:
            return False
        time.sleep(0.2)
    return True


def test_is_valid():
    test_data = [
        (('r_macguffin', 'tr'), True),
        (('r_wo', 'ru'), True),
        (('r_rocket_arena_2', 'us'), True),
        (('r_shaft_arena_1', ''), True),
        (('r_ca_2', 'ua'), True),
        (('r_ca_1', 'be'), True),
        (('r_macguffin', None), True),
        (('test', 'ru'), False),
        (('r_macguffin', 'rus'), False),
        ((None, 'ru'), False),
        ((123, 'ru'), False),
        ((None, None), False)
    ]
    for args, correct_output in test_data:
        try:
            output = leaderboard.is_valid(*args)
            assert output == correct_output
        except ParametersException:
            continue
        except:
            return False
    return True


def test_delete_user_id_field():
    user_true = [{
        'name': 'test',
        'user_id': 'test',
        'country': 'dk',
        'match_type': 2,
        'rating': '2246',
        'rank_tier': 40,
        'rank_position': 1,
        'match_count': 48,
        'match_wins': 42}]
    user_false = user_true = [{
        'name': 'test',
        'country': 'dk',
        'match_type': 2,
        'rating': '2246',
        'rank_tier': 40,
        'rank_position': 1,
        'match_count': 48,
        'match_wins': 42}]
    user_empty = [{}]
    user_without_user_id = [{
        'name': 'test',
        'country': 'dk',
        'match_type': 2,
        'rating': '2246',
        'rank_tier': 40,
        'rank_position': 1,
        'match_count': 48,
        'match_wins': 42}]

    test_data = [
        (user_true, user_without_user_id),
        (user_false, None),
        (user_empty, None)
    ]
    for user, correct_output in test_data:
        try:
            output = leaderboard.delete_user_id_field(user)
            assert output is None
        except KeyError:
            continue
        except:
            return False
    return True


def test_request_response():
    params_true = {
        'mode': 'r_macguffin',
        'offset': 0
    }
    params_false = {
        'mode': '',
        'offset': 0
    }
    test_data = [
        (params_true, '<Response [200]>'),
        (params_false, '<Response [400]>')
    ]
    for params, correct_output in test_data:
        try:
            output = leaderboard.request_response(params)
            assert str(output) == correct_output
        except ConnectException:
            continue
        except:
            return False
    return True


def test_get_result():
    json_response_1 = {
        'leaderboard': [{
            'name': 'enesy',
            'user_id': 'test',
            'country': 'dk',
            'match_type': 2,
            'rating': '2246',
            'rank_tier': 40,
            'rank_position': 1,
            'match_count': 48,
            'match_wins': 42}]
    }
    json_response_2 = {
        'leaderboard': [{
            'name': 'enesy',
            'user_id': 'test',
            'country': 'dk',
            'match_type': 2,
            'rating': '2246',
            'rank_tier': 40,
            'rank_position': 1,
            'match_count': 48,
            'match_wins': 42}]
    }
    result = {
        'leaderboard': [{
            'name': 'enesy',
            'country': 'dk',
            'match_type': 2,
            'rating': '2246',
            'rank_tier': 40,
            'rank_position': 1,
            'match_count': 48,
            'match_wins': 42}]
    }
    test_data = [
        ((3, None, None, json_response_1), result),
        ((1, None, None, json_response_2), result),
        ((1, None, 'dk', json_response_2), 1),
        ((1, None, '', json_response_2), 0),
    ]
    for input_data, correct_output in test_data:
        try:
            output = leaderboard.get_result(*input_data)
            assert output == correct_output
        except:
            return False
    return True


if __name__ == '__main__':
    tests = [
        test_is_valid,
        test_delete_user_id_field,
        test_request_response,
        test_get_result,
        test_main
    ]
    count = 0
    for test in tests:
        try:
            if test():
                print(str(test), 'ok')
                count += 1
            else:
                print(str(test), 'failed')
        except Exception as e:
            print(e)
        time.sleep(0.2)
    if count == 5:
        print('Все тесты пройдены успешно!')
    else:
        print(f'Пройдено {count} тестов из 5.')
