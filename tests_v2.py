from requests import get, post, delete
from data.users_api import users_attrs


def test_get_all_users():
    response = get('http://127.0.0.1:8080/api/v2/users').json()
    assert type(response) == dict
    assert type(response['users']) == list


def test_get_one_user():
    response = get('http://127.0.0.1:8080/api/v2/users/1').json()
    assert type(response) == dict
    assert all(key in response for key in users_attrs)


def test_get_nonexistent_user():
    response = get('http://127.0.0.1:8080/api/v2/users/0')
    assert response.status_code == 404
    assert response.json() == {'message': 'User 0 not found'}


def test_get_invalid_id():
    response = get('http://127.0.0.1:8080/api/v2/users/qq')
    assert response.status_code == 404
    assert response.json() == {'error': 'Not found'}


def test_add_empty_user():
    response = post('http://127.0.0.1:8080/api/v2/users')
    assert response.status_code == 400
    assert 'message' in response.json()


def test_add_invalid_user():
    response = post('http://127.0.0.1:8080/api/v2/users', json={'name': 'Invalid user'})
    assert response.status_code == 400
    assert 'message' in response.json()


def test_add_valid_user():
    user = {'surname': 'Test', 'name': 'User', 'age': 42, 'position': 'Yes',
            'speciality': 'No', 'address': 'module_1', 'email': 'a@a.a',
            'password': 'qwerty', 'city_from': 'Moscow'}
    response = post('http://127.0.0.1:8080/api/v2/users', json=user).json()
    assert response == {'status': 'ok'}
    last_user = get('http://127.0.0.1:8080/api/v2/users').json()['users'][-1]
    del last_user['id'], last_user['modified_date'], user['password']
    assert user == last_user


def test_delete_nonexistent_user():
    response = delete('http://127.0.0.1:8080/api/v2/users/0')
    assert response.status_code == 404
    assert response.json() == {'message': 'User 0 not found'}


def test_delete_existing_user():
    all_users = get('http://127.0.0.1:8080/api/v2/users').json()['users']
    response = delete(f'http://127.0.0.1:8080/api/v2/users/{all_users[-1]["id"]}')
    assert response.json() == {'status': 'ok'}
    assert len(all_users) == len(get('http://127.0.0.1:8080/api/v2/users').json()['users']) + 1
