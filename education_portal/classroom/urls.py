from django.urls import path

from classroom.views import new_course, delete_course, edit_course, manage_courses
from classroom.views import course_detail, my_courses
from module.views import new_module, course_modules
from page.views import new_page, page_detail
from quiz.views import (
    new_question,
    new_test,
    quiz_detail,
    take_quiz,
    submit_attempt,
    attempt_detail,
    course_test,
)

urlpatterns = [
    # courses
    path("new", new_course, name="new-course"),
    path("manage", manage_courses, name="manage-courses"),
    path("my", my_courses, name="my-courses"),
    path("<course_id>", course_detail, name="course"),
    path("<course_id>/edit", edit_course, name="edit-course"),
    path("<course_id>/delete", delete_course, name="delete-course"),
    # modules
    path("<course_id>/modules", course_modules, name="modules"),
    path("<course_id>/modules/new", new_module, name="new-module"),
    # pages
    path("<course_id>/modules/<module_id>/pages/new", new_page, name="new-page"),
    path("<course_id>/modules/<module_id>/pages/<page_id>", page_detail, name="page-detail"),
    # tests
    path("<course_id>/test", course_test, name="course-test"),
    path("<course_id>/test/new", new_test, name="new-quiz"),
    path("<course_id>/test/<quiz_id>/questions/new", new_question, name="new-question"),
    path("<course_id>/test/<quiz_id>", quiz_detail, name="quiz-detail"),
    path("<course_id>/test/<quiz_id>/take", take_quiz, name="take-quiz"),
    path("<course_id>/test/<quiz_id>/take/submit", submit_attempt, name="submit-quiz"),
    path("<course_id>/test/<quiz_id>/<attempt_id>/result", attempt_detail, name="attempt-detail"),
]
