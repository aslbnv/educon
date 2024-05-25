from django.utils import timezone

from background_task import background
from learningcontrol.models import AssignedCourses


@background(schedule=86400)
def check_deadlines():
    """Проверка курсов на просроченность каждые сутки"""
    assigned_courses = AssignedCourses.objects.filter(
        due_date__isnull=False,
        is_completed=False,
    )
    for course in assigned_courses:
        if timezone.now() > course.due_date:
            # Если текущее время больше времени сдачи, отмечаем курс просроченным
            course.is_completed = False
            course.is_expired = True
            course.save()


# Активируем задачу в фоновом режиме
check_deadlines(repeat=86400)
