from django.urls import path

from classroom.views import new_course, enroll, delete_course, edit_course, my_courses
from classroom.views import course_detail, assigned_courses
from module.views import new_module, course_modules
from page.views import new_page_module, page_detail
from quiz.views import new_question, new_quiz, quiz_detail, take_quiz, submit_attempt, attempt_detail, course_quizzes

urlpatterns = [
    # Курс
    path('newcourse', new_course, name='newcourse'),
    path('mycourses', my_courses, name='my-courses'),
    path('assigned', assigned_courses, name='courses'),
    path('<course_id>', course_detail, name='course'),
    path('<course_id>/enroll', enroll, name='enroll'),
    path('<course_id>/edit', edit_course, name='edit-course'),
    path('<course_id>/delete', delete_course, name='delete-course'),
    # Модули
    path('<course_id>/content', course_modules, name='modules'),
    path('<course_id>/modules/newmodule', new_module, name='new-module'),
    # Страницы
    path('<course_id>/modules/<module_id>/pages/newpage', new_page_module, name='new-page'),
    path('<course_id>/modules/<module_id>/pages/<page_id>', page_detail, name='page-detail'),
    # Тесты
    path('<course_id>/test', course_quizzes, name='quiz'),
    path('<course_id>/quiz/newquiz', new_quiz, name='new-quiz'),
    path('<course_id>/quiz/<quiz_id>/newquestion', new_question, name='new-question'),
    path('<course_id>/quiz/<quiz_id>/', quiz_detail, name='quiz-detail'),
    path('<course_id>/quiz/<quiz_id>/take', take_quiz, name='take-quiz'),
    path('<course_id>/quiz/<quiz_id>/take/submit', submit_attempt, name='submit-quiz'),
    path('<course_id>/quiz/<quiz_id>/<attempt_id>/result', attempt_detail, name='attempt-detail'),
]
