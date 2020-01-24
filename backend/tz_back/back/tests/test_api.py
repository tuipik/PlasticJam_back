import pytest

from django.urls import reverse
from django.utils.http import urlencode
from datetime import date, timedelta


def url_w_query_params(*args, **kwargs):
    '''
    builds url from reverse and query parameters
    '''
    params = kwargs.pop('params', {})
    url = reverse(*args, **kwargs)
    if params:
        url += '?' + urlencode(params)
    return url


@pytest.mark.django_db
def test_api_users_50_records(fill_db, client):
    records_in_db = 50
    statistics_in_db = 1
    page_size = 50 if records_in_db >= 50 else records_in_db

    fill_db(records_in_db, statistics_in_db)

    url = reverse('back:users_list')
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()['count'] == records_in_db
    assert len(response.json()['results']) == page_size


@pytest.mark.django_db
def test_api_users_51_records(fill_db, client):
    records_in_db = 51
    statistics_in_db = 1
    page_size = 50 if records_in_db >= 50 else records_in_db

    fill_db(records_in_db, statistics_in_db)

    url = reverse('back:users_list')
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()['count'] == records_in_db
    assert len(response.json()['results']) == page_size


@pytest.mark.django_db
def test_api_user_detail(fill_db, client):
    records_in_db = 1
    statistics_in_db = 1

    fill_db(records_in_db, statistics_in_db)

    url = reverse(f'back:one_user', kwargs={'pk': records_in_db})
    response = client.get(url)

    assert response.status_code == 200
    assert (len(response.json())) == 8


@pytest.mark.django_db
def test_api_nonexistent_user_detail(fill_db, client):
    records_in_db = 1
    statistics_in_db = 1

    fill_db(records_in_db, statistics_in_db)

    url = reverse(f'back:one_user', kwargs={'pk': records_in_db + 1})
    response = client.get(url)

    assert (response.json()['detail']) == 'Not found.'


params_4_tests = {
    'records_in_db': 1,
    'stat_in_db': 3,
    'dates_for_stats': ['2019-11-01',
                        (date.today() - timedelta(7)).isoformat(),
                        date.today().isoformat()]
}


@pytest.mark.django_db
def test_api_user_stat_wo_query_param(fill_db, client):
    '''
    Standart view without queryset returns records for last 7 days
    '''

    fill_db(params_4_tests['records_in_db'],
            params_4_tests['stat_in_db'],
            params_4_tests['dates_for_stats']
            )

    url = url_w_query_params('back:user_stat',
                             kwargs={'pk': params_4_tests['records_in_db']})
    response = client.get(url)
    assert len(response.json()['stats']) == 1


@pytest.mark.django_db
def test_api_user_stat_with_since_date(fill_db, client):
    '''
    Standart view with queryset since date
    returns records from this date to today
    '''

    fill_db(params_4_tests['records_in_db'],
            params_4_tests['stat_in_db'],
            params_4_tests['dates_for_stats']
            )

    url = url_w_query_params('back:user_stat',
                             kwargs={'pk': params_4_tests['records_in_db']},
                             params={'since': params_4_tests['dates_for_stats'][1]})

    response = client.get(url)
    assert len(response.json()['stats']) == 2


@pytest.mark.django_db
def test_api_user_stat_with_since_until_date(fill_db, client):
    '''
    Standart view with queryset since until date
    returns records between dates
    '''

    fill_db(params_4_tests['records_in_db'],
            params_4_tests['stat_in_db'],
            params_4_tests['dates_for_stats']
            )

    url = url_w_query_params('back:user_stat',
                             kwargs={'pk': params_4_tests['records_in_db']},
                             params={'since': params_4_tests['dates_for_stats'][0],
                                     'until': params_4_tests['dates_for_stats'][1]})

    response = client.get(url)
    assert len(response.json()['stats']) == 2

