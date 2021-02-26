from requests import get


def test_get_all_jobs():
    response = get('http://127.0.0.1:8080/api/jobs').json()
    assert type(response) == dict
    assert type(response['news']) == list


def test_get_one_job():
    response = get('http://127.0.0.1:8080/api/jobs/1').json()
    assert type(response) == dict
    assert all(key in response for key in (
        'job', 'team_leader_id', 'work_size', 'collaborators',
        'is_finished', 'start_date', 'end_date'))


def test_get_nonexistent_job():
    response = get('http://127.0.0.1:8080/api/jobs/0')
    assert response.status_code == 404
    assert response.json() == {'error': 'Not found'}


def test_get_invalid_id():
    response = get('http://127.0.0.1:8080/api/jobs/qq')
    assert response.status_code == 404
    assert response.json() == {'error': 'Not found'}
