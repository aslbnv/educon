from django import forms
from ckeditor.widgets import CKEditorWidget
from quiz.models import Quizzes, Question, Answer


class NewQuizForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Quizzes
        fields = ('title', 'description')


class NewQuestionForm(forms.ModelForm):
    question_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    points = forms.IntegerField(max_value=100, min_value=1)

    class Meta:
        model = Question
        fields = ('question_text', 'points')
