from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from learningcontrol.models import AssignedCourses


# Create your views here.
@login_required
def user_statistics(request):
    if request.user.is_staff == False:
        return redirect("index")

    completed_courses = AssignedCourses.objects.filter(is_completed=True).count()
    not_completed_courses = AssignedCourses.objects.filter(is_completed=False, is_expired=False).count()
    overdue_courses = AssignedCourses.objects.filter(is_expired=True).count()

    context = {
        'completed_courses': completed_courses,
        'not_completed_courses': not_completed_courses,
        'overdue_courses': overdue_courses,
    }

    return render(request, "user_statistics/user_statistics.html", context)
