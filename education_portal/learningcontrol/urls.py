from django.urls import path
from learningcontrol.views import LearningControl, AssignCourse

urlpatterns = [
    path('employees', LearningControl, name='employees'),
    path('<profile_id>/assigncourse', AssignCourse, name='assign-course'),
]