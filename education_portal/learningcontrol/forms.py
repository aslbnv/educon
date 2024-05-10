from django import forms
from classroom.models import Course
from learningcontrol.models import AssignedCourses
from authy.models import Profile

class AssignCourseForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all())

    class Meta:
        model = AssignedCourses
        fields = ('course',)


class UnassignCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)
        if profile:
            unique_courses = set()
            for ac in profile.assigned_courses.all():
                unique_courses.add(ac.course)
            self.fields['course'].queryset = Course.objects.filter(pk__in=[course.pk for course in unique_courses])

    class Meta:
        model = AssignedCourses
        fields = ['course']