from django.urls import path

from learningcontrol.views import employee_profiles, AssignCourse, UnassignCourse

urlpatterns = [
    path("employees", employee_profiles, name="employees"),
    path("<profile_id>/assigncourse", AssignCourse, name="assign-course"),
    path("<profile_id>/unassigncourse", UnassignCourse, name="unassign-course"),
]
