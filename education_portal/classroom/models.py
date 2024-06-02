from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid
from module.models import Module
from quiz.models import Quizzes


def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    icon = models.CharField(max_length=100, verbose_name="Icon", default="article")
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("categories", arg=[self.slug])

    def __str__(self):
        return self.title


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    syllabus = RichTextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="course_owner"
    )
    modules = models.ManyToManyField(Module)
    quizzes = models.ManyToManyField(Quizzes)

    def __str__(self):
        return self.title
