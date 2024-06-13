from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse

from quiz.forms import NewQuizForm, NewQuestionForm, QuizDetailForm
from quiz.models import Answer, Question, Quizzes, Attempter, Attempt
from module.models import Module
from classroom.models import Course
from authy.models import Profile

from datetime import datetime


def new_test(request, course_id):
    if request.user.profile.role.name != 'admin' and request.user.is_staff == False:
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


def new_question(request, course_id, quiz_id):
    if request.user.profile.role.name != 'admin' and request.user.is_staff == False:
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


def quiz_detail(request, course_id, quiz_id):
    profile = Profile.objects.get(user__id=request.user.id)
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    my_attempts = Attempter.objects.filter(quiz=quiz, user=request.user)
    max_score = sum(question.points for question in quiz.questions.all())

    if request.method == "POST":
        form = QuizDetailForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect("quiz-detail", course_id=course_id, quiz_id=quiz_id)
    else:
        form = QuizDetailForm(instance=quiz)

    context = {
        "quiz": quiz,
        "my_attempts": my_attempts,
        "course_id": course_id,
        "max_score": max_score,
        "profile": profile,
        "scores": range(1, max_score),
        "form": form,
    }

    return render(request, "quiz/quizdetail.html", context)


def take_quiz(request, course_id, quiz_id):
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    profile = Profile.objects.get(user__id=request.user.id)

    context = {
        "quiz": quiz,
        "course_id": course_id,
        "profile": profile,
    }

    return render(request, "quiz/takequiz.html", context)


def submit_attempt(request, course_id, quiz_id):
    if request.user.profile.role.name != 'user':
        return redirect("index")

    quiz = get_object_or_404(Quizzes, id=quiz_id)
    if request.method == "POST":
        questions = request.POST.getlist("question")
        answers = request.POST.getlist("answer")
        attempter = Attempter.objects.create(user=request.user, quiz=quiz, score=0)

        questions_number = len(questions)
        resolved_questions_number = 0

        # check answer for correctness
        for q, a in zip(questions, answers):
            question = Question.objects.get(id=q)
            answer = Answer.objects.get(id=a)

            # create attempt
            Attempt.objects.create(
                quiz=quiz, attempter=attempter, question=question, answer=answer
            )

            # if answer is correct, increase counter
            if answer.is_correct:
                resolved_questions_number += 1

        # mark course as completed and set completion time if
        # count of doned answer equal to total answers count
        if quiz.points_to_pass:
            questions_number = quiz.points_to_pass
        if resolved_questions_number >= questions_number:
            profile = Profile.objects.get(user=request.user)
            course = get_object_or_404(Course, id=course_id)
            current_assigned_course = profile.assigned_courses.filter(course=course).first()

            if current_assigned_course:
                current_assigned_course.is_completed = True
                current_assigned_course.completion_date = datetime.now()
                current_assigned_course.save()

            attempter.test_completed = True
            attempter.save()

        # set score of attempter, if score is equal to amount of doned questions
        attempter.score = resolved_questions_number
        attempter.save()

        return redirect(
            reverse("quiz-detail", kwargs={"course_id": course_id, "quiz_id": quiz_id})
        )


def attempt_detail(request, course_id, module_id, quiz_id, attempt_id):
    if request.user.profile.role.name != 'user':
        return redirect("index")

    user = request.user
    quiz = get_object_or_404(Quizzes, id=quiz_id)
    attempts = Attempt.objects.filter(quiz=quiz, attempter__user=user)

    context = {
        "quiz": quiz,
        "attempts": attempts,
        "course_id": course_id,
    }

    return render(request, "quiz/attemptdetail.html", context)


def course_test(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    teacher_mode = False
    if user == course.user:
        teacher_mode = True

    context = {
        "teacher_mode": teacher_mode,
        "course": course,
    }

    return render(request, "quiz/quiz.html", context)
