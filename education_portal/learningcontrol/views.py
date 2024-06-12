from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from learningcontrol.models import AssignedCourses
from learningcontrol.forms import AssignCourseForm, UnassignCourseForm, EmployeeLastnameFilterForm
from authy.models import Profile
from quiz.models import Attempter


@login_required
def employee_profiles(request):
    if request.user.is_staff == False:
        return redirect("index")

    form = EmployeeLastnameFilterForm(request.GET)
    last_name = request.GET.get("last_name")
    last_name_format = ""
    if last_name != None:
        for i in range(len(last_name)):
            if i == 0:
                last_name_format += last_name[i].upper()
            else:
                last_name_format += last_name[i].lower()

    profiles = Profile.objects.filter(role="user")
    if last_name:
        profiles = profiles.filter(user__last_name__icontains=last_name_format)

    context = {
        "users": User.objects.filter(is_staff=False),
        "profiles": profiles,
        "form": form,
    }

    return render(request, "learningcontrol/learningcontrol.html", context)


@login_required
def assign_course(request, profile_id):
    if request.user.is_staff == False:
        return redirect("index")
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == "POST":
        form = AssignCourseForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data.get("course")
            due_date = form.cleaned_data.get("due_date")
            if profile.assigned_courses.filter(course=course).exists():
                messages.error(request, "Этот курс уже назначен данному пользователю.")
            else:
                if due_date:
                    ac = AssignedCourses.objects.create(
                        course=course, due_date=due_date
                    )
                else:
                    ac = AssignedCourses.objects.create(course=course)
                profile.assigned_courses.add(ac)
                profile.save()
                return redirect("employees")
    else:
        form = AssignCourseForm()

    context = {
        "form": form,
    }

    return render(request, "learningcontrol/assigncourse.html", context)


@login_required
def unassign_course(request, profile_id):
    if request.user.is_staff == False:
        return redirect("index")
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == "POST":
        form = UnassignCourseForm(request.POST, profile=profile)
        if form.is_valid():
            course = form.cleaned_data.get("course")
            profile.assigned_courses.filter(course=course).delete()
            # also delete user attempts in course quiz
            quizzes = course.quizzes.all()
            # get user and quiz
            user = profile.user
            if quizzes.exists():
                quiz = quizzes.first()
            else:
                quiz = None
            # delete attempters
            if quiz and user:
                attempters = Attempter.objects.filter(quiz=quiz, user=user)
                if attempters.exists():
                    attempters.delete()
            return redirect("employees")
    else:
        form = UnassignCourseForm(profile=profile)

    context = {
        "form": form,
    }

    return render(request, "learningcontrol/unassigncourse.html", context)
