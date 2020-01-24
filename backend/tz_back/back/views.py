from datetime import timedelta

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from back import models as m
from back import serialilzers as s
from django.conf import settings

from django.shortcuts import render


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UsersView(ListAPIView):
    queryset = m.User.objects.all()
    serializer_class = s.UserSerializer
    pagination_class = StandardResultsSetPagination


class OneUserView(RetrieveAPIView):
    queryset = m.User.objects.all()
    serializer_class = s.UserSerializer


class UserStatisticsView(APIView):

    def get_dates_from_valid_data(self, valid_data):
        since = valid_data.get('since')
        until = valid_data.get('until')
        today = settings.TODAY_DATE
        if not since:
            since = today - timedelta(6)
        if not until:
            until = today
        return since, until

    def get(self, request, pk):
        query_params_serializer = s.UserStaristicsQueryParamsSerializer(
            data=request.query_params)
        if not query_params_serializer.is_valid():
            return Response({'errors': query_params_serializer.errors})
        validated_data = query_params_serializer.validated_data
        since, until = self.get_dates_from_valid_data(validated_data)
        statistics = m.UserStatistics.filter_by_user(pk).filter(
            date__gte=since, date__lte=until).order_by('date')
        serializer = s.UserStatisticsSerializer(statistics, many=True)
        return Response({"stats": serializer.data})


def index(request):
    return render(request, 'build/index.html')



