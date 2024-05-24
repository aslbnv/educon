from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse

from quiz.forms import NewQuizForm, NewQuestionForm
from quiz.models import Answer, Question, Quizzes, Attempter, Attempt
from module.models import Module
from classroom.models import Course
from authy.models import Profile

from datetime import datetime


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


def QuizDetail(request, course_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    my_attempts = Attempter.objects.filter(quiz=quiz, user=user)
    max_score = sum(question.points for question in quiz.questions.all())

    context = {
        "quiz": quiz,
        "my_attempts": my_attempts,
        "course_id": course_id,
        "max_score": max_score,
    }

    return render(request, "quiz/quizdetail.html", context)


def TakeQuiz(request, course_id, quiz_id):
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    profile = Profile.objects.get(user__id=request.user.id)

    context = {
        "quiz": quiz,
        "course_id": course_id,
        "profile": profile,
    }

    return render(request, "quiz/takequiz.html", context)


def SubmitAttempt(request, course_id, quiz_id):
    quiz = get_object_or_404(Quizzes, id=quiz_id)

    if request.method == "POST":
        questions = request.POST.getlist("question")
        answers = request.POST.getlist("answer")
        attempter = Attempter.objects.create(user=request.user, quiz=quiz, score=0)

        questions_number = len(questions)
        resolved_questions_number = 0

        # Checking questions for correctness
        for q, a in zip(questions, answers):
            question = Question.objects.get(id=q)
            answer = Answer.objects.get(id=a)

            # Create an attempt object
            Attempt.objects.create(
                quiz=quiz, attempter=attempter, question=question, answer=answer
            )

            # Checking to see if the question is resolved
            if answer.is_correct:
                resolved_questions_number += 1

        # Mark the course as completed and indicate the date of completion
        if resolved_questions_number == questions_number:
            profile = Profile.objects.get(user=request.user)
            course = get_object_or_404(Course, id=course_id)
            current_assigned_course = profile.assigned_courses.filter(
                course=course
            ).first()

            if current_assigned_course:
                current_assigned_course.is_completed = True
                current_assigned_course.completion_date = datetime.now()
                current_assigned_course.save()

            attempter.test_completed = True
            attempter.save()

        # Assigning the number of solved questions to the attempter score
        attempter.score = resolved_questions_number
        attempter.save()

        return redirect(
            reverse("quiz-detail", kwargs={"course_id": course_id, "quiz_id": quiz_id})
        )


def AttemptDetail(request, course_id, module_id, quiz_id, attempt_id):
    user = request.user
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    attempts = Attempt.objects.filter(quiz=quiz, attempter__user=user)

    context = {
        "quiz": quiz,
        "attempts": attempts,
        "course_id": course_id,
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
