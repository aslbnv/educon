from django.db import models

from classroom.models import Course


class AssignedCourses(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.course} - Completed: {self.is_completed}"
