import datetime as dt
from requests import get, post, delete
from data.users_api import users_attrs
from data.jobs_api import job_fields, DATE_FORMAT

USERS_API_URL = 'http://127.0.0.1:8080/api/v2/users/'
JOBS_API_URL = 'http://127.0.0.1:8080/api/v2/jobs/'


# USERS API
def test_get_all_users():
    response = get(USERS_API_URL).json()
    assert type(response) == dict
    assert type(response['users']) == list


def test_get_one_user():
    response = get(USERS_API_URL + '1').json()
    assert type(response) == dict
    assert all(key in response for key in users_attrs)


def test_get_nonexistent_user():
    response = get(USERS_API_URL + '0')
    assert response.status_code == 404
    assert response.json() == {'message': 'User 0 not found'}


def test_get_user_by_invalid_id():
    response = get(USERS_API_URL + 'qq')
    assert response.status_code == 404
    assert response.json() == {'error': 'Not found'}


def test_add_empty_user():
    response = post(USERS_API_URL)
    assert response.status_code == 400
    assert 'message' in response.json()


def test_add_invalid_user():
    response = post(USERS_API_URL, json={'name': 'Invalid user'})
    assert response.status_code == 400
    assert 'message' in response.json()


def test_add_valid_user():
    user = {'surname': 'Test', 'name': 'User', 'age': 42, 'position': 'Yes',
            'speciality': 'No', 'address': 'module_1', 'email': 'a@a.a',
            'password': 'qwerty', 'city_from': 'Moscow'}
    response = post(USERS_API_URL, json=user).json()
    assert response == {'status': 'ok'}
    last_user = get(USERS_API_URL).json()['users'][-1]
    del last_user['id'], last_user['modified_date'], user['password']
    assert user == last_user


def test_delete_nonexistent_user():
    response = delete(USERS_API_URL + '0')
    assert response.status_code == 404
    assert response.json() == {'message': 'User 0 not found'}


def test_delete_existing_user():
    all_users = get(USERS_API_URL).json()['users']
    response = delete(f'{USERS_API_URL}{all_users[-1]["id"]}')
    assert response.json() == {'status': 'ok'}
    assert len(all_users) == len(get(USERS_API_URL).json()['users']) + 1


# JOBS API
def test_get_all_jobs():
    response = get(JOBS_API_URL).json()
    assert type(response) == dict
    assert type(response['jobs']) == list


def test_get_one_job():
    response = get(JOBS_API_URL + '1').json()
    assert type(response) == dict
    assert all(key in response for key in job_fields + ('id',))


def test_get_nonexistent_job():
    response = get(JOBS_API_URL + '0')
    assert response.status_code == 404
    assert response.json() == {'message': 'Jobs 0 not found'}


def test_get_job_by_invalid_id():
    response = get(JOBS_API_URL + 'qq')
    assert response.status_code == 404
    assert response.json() == {'error': 'Not found'}


def test_add_empty_job():
    response = post(JOBS_API_URL)
    assert response.status_code == 400
    assert 'message' in response.json()


def test_add_invalid_job():
    response = post(JOBS_API_URL, json={'job': 'Invalid job'})
    assert response.status_code == 400
    assert 'message' in response.json()


def test_add_valid_job():
    job = {'job': 'Test job', 'team_leader_id': 1, 'work_size': 10,
           'collaborators': '2, 3', 'is_finished': False,
           'start_date': (dt.datetime.now()).strftime('%Y-%m-%d %H:%M:%S'), 'categories': '[]',
           'end_date': (dt.datetime.now() + dt.timedelta(hours=10)).strftime(DATE_FORMAT)}
    response = post(JOBS_API_URL, json=job).json()
    assert response == {'status': 'ok'}
    job['categories'] = []
    last_job = get(JOBS_API_URL).json()['jobs'][-1]
    del last_job['id']
    assert job == last_job


def test_delete_nonexistent_job():
    response = delete(JOBS_API_URL + '0')
    assert response.status_code == 404
    assert response.json() == {'message': 'Jobs 0 not found'}


def test_delete_existing_job():
    all_jobs = get(JOBS_API_URL).json()['jobs']
    response = delete(f'{JOBS_API_URL}{all_jobs[-1]["id"]}')
    assert response.json() == {'status': 'ok'}
    assert len(all_jobs) == len(get(JOBS_API_URL).json()['jobs']) + 1
