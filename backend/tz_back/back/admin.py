from django.contrib import admin

from .models import User, UserStatistics


admin.site.register(User)
admin.site.register(UserStatistics)
