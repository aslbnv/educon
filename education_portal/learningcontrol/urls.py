from django.urls import path
from learningcontrol.views import LearningControl, AssignCourse, UnassignCourse

urlpatterns = [
    path('employees', LearningControl, name='employees'),
    path('<profile_id>/assigncourse', AssignCourse, name='assign-course'),
    path('<profile_id>/unassigncourse', UnassignCourse, name='unassign-course'),
]