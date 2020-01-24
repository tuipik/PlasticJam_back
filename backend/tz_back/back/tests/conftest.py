import pytest

from back.models import User, UserStatistics


@pytest.fixture
def fill_db():
    def database_fill(users_count, stat_count, test_date=None):
        for num in range(users_count):
            user = User.objects.create(
                first_name=f"testName{num+1}",
                last_name=f"testLastName{num+1}",
                email=f"testEmail{num+1}@example.com",
                gender=f"male",
                ip_address="45.225.25.145"
            )
            for st_num in range(stat_count):
                statistics = UserStatistics.objects.create(
                    user=User.objects.get(id=num+1),
                    date=test_date[st_num]
                        if test_date and len(test_date) == stat_count
                        else f"2019-10-{1+st_num if st_num < 28 else 1}",
                    page_views=1,
                    clicks=1
                )
    return database_fill
