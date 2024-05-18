from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from datetime import datetime

from quiz.forms import NewQuizForm, NewQuestionForm
from quiz.models import Answer, Question, Quizzes, Attempter, Attempt
from module.models import Module
from classroom.models import Course
from authy.models import Profile


# Создать новый тест
def NewQuiz(request, course_id):
    if request.user.is_staff == False:
        return redirect("index")

    user = request.user
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = NewQuizForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")
            quiz = Quizzes.objects.create(
                user=user, title=title, description=description
            )
            course.quizzes.add(quiz)
            course.save()
            return redirect("new-question", course_id=course_id, quiz_id=quiz.id)
    else:
        form = NewQuizForm()

    context = {
        "form": form,
    }
    return render(request, "quiz/newquiz.html", context)


# Создать новый вопрос
def NewQuestion(request, course_id, quiz_id):
    if request.user.is_staff == False:
        return redirect("index")

    user = request.user
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    if request.method == "POST":
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data.get("question_text")
            points = 1
            answer_text = request.POST.getlist("answer_text")
            is_correct = request.POST.getlist("is_correct")
            question = Question.objects.create(
                question_text=question_text, user=user, points=points
            )

            for a, c in zip(answer_text, is_correct):
                answer = Answer.objects.create(answer_text=a, is_correct=c, user=user)
                question.answers.add(answer)
                question.save()
                quiz.questions.add(question)
                quiz.save()
            return redirect("new-question", course_id=course_id, quiz_id=quiz.id)
    else:
        form = NewQuestionForm()

    context = {
        "form": form,
        "quiz_id": quiz_id,
        "course_id": course_id,
    }
    return render(request, "quiz/newquestion.html", context)


# Подробности теста
def QuizDetail(request, course_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    my_attempts = Attempter.objects.filter(quiz=quiz, user=user)

    context = {
        "quiz": quiz,
        "my_attempts": my_attempts,
        "course_id": course_id,
    }
    return render(request, "quiz/quizdetail.html", context)


# Пройти тест
def TakeQuiz(request, course_id, quiz_id):
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    profile = Profile.objects.get(user__id=request.user.id)

    context = {
        "quiz": quiz,
        "course_id": course_id,
        "profile": profile,
    }

    return render(request, "quiz/takequiz.html", context)


# Отправить решение
def SubmitAttempt(request, course_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    earned_points = 0
    is_completed = False

    profile = Profile.objects.get(user=request.user)
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        questions = request.POST.getlist("question")
        answers = request.POST.getlist("answer")
        attempter = Attempter.objects.create(user=user, quiz=quiz, score=0)

        for q, a in zip(questions, answers):
            question = Question.objects.get(id=q)
            answer = Answer.objects.get(id=a)
            Attempt.objects.create(
                quiz=quiz, attempter=attempter, question=question, answer=answer
            )
            if answer.is_correct == True:
                is_completed = True
                earned_points += question.points
                attempter.score += earned_points
                attempter.save()
            else:
                is_completed = False
        if is_completed == True:
            assigned_course = profile.assigned_courses.filter(course=course).first()
            if assigned_course:
                assigned_course.is_completed = True
                assigned_course.completion_date = datetime.now()
                assigned_course.save()
            attempter.test_completed = True
            attempter.save()
        attempter.score /= 2
        attempter.save()

        return redirect("index")


# Подробности решения
def AttemptDetail(request, course_id, module_id, quiz_id, attempt_id):
    user = request.user
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    attempts = Attempt.objects.filter(quiz=quiz, attempter__user=user)

    context = {
        "quiz": quiz,
        "attempts": attempts,
        "course_id": course_id,
        "module_id": module_id,
    }
    return render(request, "quiz/attemptdetail.html", context)


def CourseQuizzes(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    teacher_mode = False
    if user == course.user:
        teacher_mode = True

    context = {"teacher_mode": teacher_mode, "course": course}

    return render(request, "quiz/quiz.html", context)
