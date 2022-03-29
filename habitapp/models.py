from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.template.defaultfilters import slugify
from django.utils import timezone
from calendar import HTMLCalendar
from datetime import date
from itertools import groupby


class User(AbstractUser):
    def __repr__(self):
        return f"<User username={self.username}>"

    def __str__(self):
        return self.username


class Habit(models.Model):
    name = models.CharField(max_length=200)
    goal = models.IntegerField(default=0)
    description = models.TextField(max_length=1000)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="habit_user"
    )
    slug = models.SlugField(
        max_length=200,
        null=True,
        blank=True,
        unique=True,
    )
    unit = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

    def save(self):
        self.slug = slugify(self.name)
        super().save()


class Record(models.Model):
    date = models.DateField(default=datetime.now, verbose_name="date for plan")
    goal_number = models.IntegerField(default=0)
    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, null=True, blank=True, related_name="habit"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="habit_record_user",
    )

    def __str__(self):
        return f"{self.goal_number} {self.date}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "date", "habit"], name="once_a_day")
        ]
