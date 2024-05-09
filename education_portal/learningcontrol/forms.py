from django import forms
from classroom.models import Course
from learningcontrol.models import AssignedCourses

class AssignCourseForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all())

    class Meta:
        model = AssignedCourses
        fields = ('course',)