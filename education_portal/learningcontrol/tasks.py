from django.utils import timezone
from background_task import background
from learningcontrol.models import AssignedCourses


@background(schedule=60)  # Проверка каждую минуту
def check_deadlines():
    assigned_courses = AssignedCourses.objects.filter(
        due_date__isnull=False,
        is_completed=False,
    )
    for course in assigned_courses:
        if timezone.now() > course.due_date:
            # Если текущее время превышает дедлайн, обновляем статус курса
            course.is_completed = False
            course.is_expired = True
            course.save()
