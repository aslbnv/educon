from django.urls import path

from learningcontrol.views import employee_profiles, assign_course, unassign_course

urlpatterns = [
    path("employees", employee_profiles, name="employees"),
    path("<profile_id>/assigncourse", assign_course, name="assign-course"),
    path("<profile_id>/unassigncourse", unassign_course, name="unassign-course"),
]
