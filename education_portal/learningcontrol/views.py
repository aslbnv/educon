from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from authy.models import Profile
from learningcontrol.models import AssignedCourses
from learningcontrol.forms import AssignCourseForm, UnassignCourseForm


# Create your views here.
@login_required
def LearningControl(request):
    users = User.objects.filter(is_staff=False)
    profiles = Profile.objects.filter(role='user')

    context = {
        'users': users,
        'profiles': profiles,
    }

    return render(request, 'learningcontrol/learningcontrol.html', context)


@login_required
def AssignCourse(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        form = AssignCourseForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data.get('course')
            ac = AssignedCourses.objects.create(course=course)
            profile.assigned_courses.add(ac)
            profile.save()
            return redirect('employees')
    else:
        form = AssignCourseForm()

    context = {
        'form': form,
    }

    return render(request, 'learningcontrol/assigncourse.html', context)


@login_required
def UnassignCourse(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        form = UnassignCourseForm(request.POST, profile=profile)
        if form.is_valid():
            course = form.cleaned_data.get('course')
            profile.assigned_courses.filter(course=course).delete()
            return redirect('employees')
    else:
        form = UnassignCourseForm(profile=profile)

    context = {
        'form': form,
    }

    return render(request, 'learningcontrol/unassigncourse.html', context)