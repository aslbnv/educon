from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Answer(models.Model):
    """Класс Answer используется для представления ответа на вопрос"""

    answer_text = models.CharField(max_length=900)
    is_correct = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text


class Question(models.Model):
    """Класс Question используется для представления вопроса"""

    question_text = models.CharField(max_length=900)
    answers = models.ManyToManyField(Answer)
    points = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class Quizzes(models.Model):
    """Класс Quizzes используется для представления тестов
    Тест - список вопросов и прилагающихся к ним ответов"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = RichTextField()
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title


class Attempter(models.Model):
    """Класс Attempter используется для представления экзаменуемого пользователя
    (проходящего тест в данный момент)"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    test_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Attempt(models.Model):
    """Класс Attempt используется для представления попытки решения теста
    экзаменуемого пользователя"""

    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    attempter = models.ForeignKey(Attempter, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.attempter.user.username + " - " + self.answer.answer_text
