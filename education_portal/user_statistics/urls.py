from django.urls import path

from user_statistics.views import user_statistics

urlpatterns = [
    path("", user_statistics, name="user-statistics"),
]
