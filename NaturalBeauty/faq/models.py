from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True
    )
    image = models.ImageField()
    description = models.CharField(
        max_length=250,
    )

    def __str__(self):
        return self.name


class Response(models.Model):
    response = models.TextField(
        max_length=1000,
    )
    responder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="responder"
    )

    def __str__(self):
        return self.response


class Question(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category',
        blank=False,
        null=False,
    )
    question = models.CharField(
        max_length=250,
    )
    response = models.ManyToManyField(
        Response,
        blank=True,
        related_name="response_of_question"
    )
    visitor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="visitor"
    )
    locked = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.question

# EOF
