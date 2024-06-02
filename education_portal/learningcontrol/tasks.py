from django.utils import timezone

from background_task import background
from learningcontrol.models import AssignedCourses


@background(schedule=86400)
def check_deadlines():
    """Method that check all assigned courses for overdue once in day"""
    assigned_courses = AssignedCourses.objects.filter(
        due_date__isnull=False,
        is_completed=False,
    )
    for course in assigned_courses:
        # if current time bigger than due date, mark course as overdue
        if timezone.now() > course.due_date:
            course.is_completed = False
            course.is_expired = True
            course.save()


# activate task in background mode once in day
check_deadlines(repeat=86400)
