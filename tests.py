import datetime as dt
from requests import get, post
from data.jobs_api import job_fields, DATE_FORMAT


def test_get_all_jobs():
    response = get('http://127.0.0.1:8080/api/jobs').json()
    assert type(response) == dict
    assert type(response['jobs']) == list


def test_get_one_job():
    response = get('http://127.0.0.1:8080/api/jobs/1').json()
    assert type(response) == dict
    assert all(key in response for key in job_fields)


def test_get_nonexistent_job():
    response = get('http://127.0.0.1:8080/api/jobs/0')
    assert response.status_code == 404
    assert response.json() == {'error': 'Not found'}


def test_get_invalid_id():
    response = get('http://127.0.0.1:8080/api/jobs/qq')
    assert response.status_code == 404
    assert response.json() == {'error': 'Not found'}


def test_add_empty_job():
    response = post('http://127.0.0.1:8080/api/jobs')
    assert response.status_code == 400
    assert response.json() == {'error': 'Bad request'}


def test_add_invalid_job():
    response = post('http://127.0.0.1:8080/api/jobs', json={'job': 'Invalid job'})
    assert response.status_code == 400
    assert response.json() == {'error': 'Bad request'}


def test_add_valid_job():
    job = {'job': 'Test job', 'team_leader_id': 1, 'work_size': 10,
           'collaborators': '2, 3', 'is_finished': False,
           'start_date': (dt.datetime.now()).strftime('%Y-%m-%d %H:%M:%S'), 'categories': [],
           'end_date': (dt.datetime.now() + dt.timedelta(hours=10)).strftime(DATE_FORMAT)}
    response = post('http://127.0.0.1:8080/api/jobs', json=job).json()
    assert response == {'status': 'ok'}
    assert job in get('http://127.0.0.1:8080/api/jobs').json()['jobs']
