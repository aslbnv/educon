from django.urls import path

from classroom.views import NewCourse, Enroll, DeleteCourse, EditCourse, MyCourses
from classroom.views import CourseDetail, AssignedCourses
from module.views import NewModule, CourseModules
from page.views import NewPageModule, PageDetail
from quiz.views import NewQuestion, NewQuiz, QuizDetail, TakeQuiz, SubmitAttempt, AttemptDetail, CourseQuizzes

urlpatterns = [
    # Курс
    path('newcourse', NewCourse, name='newcourse'),
    path('mycourses', MyCourses, name='my-courses'),
    path('assigned', AssignedCourses, name='courses'),
    path('<course_id>', CourseDetail, name='course'),
    path('<course_id>/enroll', Enroll, name='enroll'),
    path('<course_id>/edit', EditCourse, name='edit-course'),
    path('<course_id>/delete', DeleteCourse, name='delete-course'),
    # Модули
    path('<course_id>/content', CourseModules, name='modules'),
    path('<course_id>/modules/newmodule', NewModule, name='new-module'),
    # Страницы
    path('<course_id>/modules/<module_id>/pages/newpage', NewPageModule, name='new-page'),
    path('<course_id>/modules/<module_id>/pages/<page_id>', PageDetail, name='page-detail'),
    # Тесты
    path('<course_id>/test', CourseQuizzes, name='quiz'),
    path('<course_id>/quiz/newquiz', NewQuiz, name='new-quiz'),
    path('<course_id>/quiz/<quiz_id>/newquestion', NewQuestion, name='new-question'),
    path('<course_id>/quiz/<quiz_id>/', QuizDetail, name='quiz-detail'),
    path('<course_id>/quiz/<quiz_id>/take', TakeQuiz, name='take-quiz'),
    path('<course_id>/quiz/<quiz_id>/take/submit', SubmitAttempt, name='submit-quiz'),
    path('<course_id>/quiz/<quiz_id>/<attempt_id>/result', AttemptDetail, name='attempt-detail'),
]
