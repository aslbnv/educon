from django import forms
from ckeditor.widgets import CKEditorWidget
from quiz.models import Quizzes, Question, Answer


class NewQuizForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "validate"}),
        required=True,
    )
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Quizzes
        fields = ("title", "description")


class NewQuestionForm(forms.ModelForm):
    question_text = forms.CharField(
        widget=forms.TextInput(attrs={"class": "validate"}),
        required=True,
    )

    class Meta:
        model = Question
        fields = ("question_text",)


class QuizDetailForm(forms.ModelForm):
    class Meta:
        model = Quizzes
        fields = ["points_to_pass"]
        labels = {
            "points_to_pass": "",
        }
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            max_score = self.instance.questions.count()  # get questions count
            self.fields['points_to_pass'].widget.attrs['min'] = 1
            self.fields['points_to_pass'].widget.attrs['max'] = max_score
