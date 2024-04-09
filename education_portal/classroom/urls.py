from django.urls import path
from classroom.views import Categories, CategoryCourses, NewCourse, Enroll, DeleteCourse, EditCourse, MyCourses, \
    CourseDetail

from module.views import NewModule, CourseModules
from page.views import NewPageModule, PageDetail

urlpatterns = [
    # Course - Classroom Views
    path('newcourse/', NewCourse, name='newcourse'),
    path('mycourses/', MyCourses, name='my-courses'),
    path('categories/', Categories, name='categories'),
    path('categories/<category_slug>', CategoryCourses, name='category-courses'),
    path('<course_id>/', CourseDetail, name='course'),
    path('<course_id>/enroll', Enroll, name='enroll'),
    path('<course_id>/edit', EditCourse, name='edit-course'),
    path('<course_id>/delete', DeleteCourse, name='delete-course'),
    # Modules
    path('<course_id>/modules', CourseModules, name='modules'),
    path('<course_id>/modules/newmodule', NewModule, name='new-module'),
    # Pages
    path('<course_id>/modules/<module_id>/newpage', NewPageModule, name='new-page'),
    path('<course_id>/modules/<module_id>/<page_id>', PageDetail, name='page-detail'),
]
