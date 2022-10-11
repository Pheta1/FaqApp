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


class Faq(models.Model):
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
    visitor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="visitor"
    )
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
    locked = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.question

# EOF
