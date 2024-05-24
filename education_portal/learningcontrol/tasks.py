from django.utils import timezone

from background_task import background
from learningcontrol.models import AssignedCourses


@background(schedule=60)
def check_deadlines():
    """A method used to check whether users are past due on their courses. Run every 60 secondsF"""
    assigned_courses = AssignedCourses.objects.filter(
        due_date__isnull=False,
        is_completed=Falsтe,
    )
    for course in assigned_courses:
        if timezone.now() > course.due_date:
            # If current time is bigger then deadline time, update course status
            course.is_completed = False
            course.is_expired = True
            course.save()


# Task activation
check_deadlines(repeat=60)
