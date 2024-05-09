from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from authy.models import Profile


# Create your views here.
@login_required
def LearningControl(request):
    users = User.objects.filter(is_staff=False)
    profiles = Profile.objects.filter(role='user')

    context = {
        'users': users,
    }

    return render(request, 'learningcontrol/learningcontrol.html', context)


@login_required
def AssignCourse(request):

    return render(request, 'learningcontrol/assigncourse.html')