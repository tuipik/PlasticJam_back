from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from .views import UserStatisticsView, UsersView, OneUserView, index

app_name = "back"

urlpatterns = [
    url(r'^users/$', UsersView.as_view(), name='users_list'),
    url(r'^users/(?P<pk>\d+)/$', OneUserView.as_view(), name='user_detail'),
    url(r'^stats/(?P<pk>\d+)/$', UserStatisticsView.as_view(), name='user_stat'),
    url(r'^', index),
]
