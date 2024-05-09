from django.db import models

from classroom.models import Course

class AssignedCourses(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course} - Completed: {self.is_completed}"