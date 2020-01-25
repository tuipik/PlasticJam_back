import pytest

from django.urls import reverse
from django.utils.http import urlencode
from datetime import date, timedelta

from back.models import User, UserStatistics


def build_url_with_query_params(*args, **kwargs):
    """
    builds url from reverse and query parameters
    """
    params = kwargs.pop('params', {})
    url = reverse(*args, **kwargs)
    if params:
        url += '?' + urlencode(params)
    return url


@pytest.mark.django_db
@pytest.mark.parametrize("test_input,expected", [(50, 50), (51, 50),
                                                 (0, 0), (1, 1), (120, 50)])
def test_api_users_records_counter(fill_db, client, test_input, expected):
    records_in_db = test_input
    statistics_in_db = 1
    page_size = expected

    fill_db(records_in_db, statistics_in_db)

    url = build_url_with_query_params('back:users_list')
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()['count'] == test_input
    assert len(response.json()['results']) == page_size


@pytest.mark.django_db
def test_api_user_detail(fill_db, client):
    records_in_db = 1
    statistics_in_db = 1

    fill_db(records_in_db, statistics_in_db)

    user_from_db = User.objects.get(id=records_in_db)

    url = build_url_with_query_params('back:user_detail',
                                      kwargs={'pk': records_in_db})
    response = client.get(url)

    assert response.status_code == 200
    assert user_from_db.first_name == response.json()['first_name']
    assert user_from_db.last_name == response.json()['last_name']
    assert user_from_db.email == response.json()['email']
    assert user_from_db.gender == response.json()['gender']
    assert user_from_db.ip_address == response.json()['ip_address']


@pytest.mark.django_db
def test_api_nonexistent_user_detail(fill_db, client):
    records_in_db = 1
    statistics_in_db = 1

    fill_db(records_in_db, statistics_in_db)

    url = build_url_with_query_params('back:user_detail',
                                      kwargs={'pk': records_in_db + 1})
    response = client.get(url)

    assert (response.json()['detail']) == 'Not found.'


dates = ['2019-11-01',                                  # random date
         (date.today() - timedelta(7)).isoformat(),     # 8 days before today
         date.today().isoformat()]                      # today


def date_filter_queryset_len(d1=None, d2=None):
    if d1 is None and d2 is None:
        week = (date.today() - timedelta(6)).isoformat()
        query = UserStatistics.objects.filter(
            date__range=[week, dates[2]])

    elif d1 and d2 is None:
        query = UserStatistics.objects.filter(
            date__range=[d1, dates[2]])

    else:
        query = UserStatistics.objects.filter(
            date__range=[d1, d2])

    return len(query)


@pytest.mark.django_db
@pytest.mark.parametrize("dates_for_stats, since, until",
                         [(dates, None, None),
                          (dates, dates[1], None),
                          (dates, dates[0], dates[1])
                          ])
def test_api_user_stat_with_query_param(fill_db, client, dates_for_stats,
                                        since, until):

    records_in_db = 1
    stat_in_db = 3

    fill_db(records_in_db,
            stat_in_db,
            dates_for_stats
            )

    url = build_url_with_query_params('back:user_stat',
                                      kwargs={'pk': records_in_db},
                                      params={'since': since if since else '',
                                              'until': until if until else ''}
                                      )
    response = client.get(url)

    expected = date_filter_queryset_len(since, until)

    assert len(response.json()['stats']) == expected
