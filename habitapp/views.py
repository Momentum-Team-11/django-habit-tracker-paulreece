from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Habit, Record
from .forms import HabitForm, RecordForm
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
import calendar
from calendar import MONDAY, SUNDAY, HTMLCalendar, month_name
from .charts import (
    months,
    colorPrimary,
    colorSuccess,
    colorDanger,
    generate_color_palette,
    get_year_dict,
)
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg


def base_login(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    return render(request, "base.html")


@login_required(login_url="auth_login")
def homepage(
    request,
):
    habits = Habit.objects.all()
    records = Record.objects.all()
    return render(request, "homepage.html", {"habits": habits, "records": records})


@login_required
def habit_detail(request, slug):
    labels = []
    data = []
    json_list = []
    habit = get_object_or_404(Habit, slug=slug)
    records = Record.objects.all().filter(habit_id=habit.id).order_by("date")[:30]
    attempt_avg = (
        Record.objects.all().filter(habit_id=habit.id).aggregate(Avg("goal_number"))
    )
    for record in records:
        labels.append(str(record.date))
        data.append(record.goal_number)
        start = record.date.strftime("%Y-%m-%d")
        end = record.date.strftime("%Y-%m-%d")
        title = str(record.goal_number) + " " + habit.unit
        json_entry = {"title": title, "start": start, "end": end}
        json_list.append(json_entry)

    return render(
        request,
        "habit_detail.html",
        {
            "habit": habit,
            "records": records,
            "labels": labels,
            "data": data,
            "json_list": json_list,
            "attempt_avg": attempt_avg,
        },
        print(attempt_avg),
    )


@login_required
def add_habit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "GET":
        form = HabitForm()
    else:
        form = HabitForm(data=request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user_id = user.id
            habit.save()
            return redirect(to="homepage")

    return render(request, "add_habit.html", {"form": form, "user": user})


@login_required
def delete_habit(request, slug):
    habit = get_object_or_404(Habit, slug=slug)
    if request.method == "POST":
        habit.delete()
        return redirect(to="homepage")

    return render(request, "delete_habit.html", {"habit": habit})


@login_required
def edit_habit(request, slug):
    habit = get_object_or_404(Habit, slug=slug)
    user = get_object_or_404(User)
    if request.method == "POST":
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user_id = user.id
            habit.save()
            return redirect(to="homepage")
    else:
        form = HabitForm(instance=habit)
    return render(
        request, "edit_habit.html", {"form": form, "habit": habit, "user": user}
    )


@login_required
def add_record(request, slug):
    habit = get_object_or_404(Habit, slug=slug)
    user = get_object_or_404(User)
    if request.method == "GET":
        form = RecordForm()
    else:
        form = RecordForm(data=request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user_id = user.id
            record.habit_id = habit.id
            try:
                record.save()
            except IntegrityError:
                return redirect(to="habit_detail", slug=habit.slug)
        return redirect(to="habit_detail", slug=habit.slug)

    return render(request, "add_record.html", {"form": form, "habit": habit})


@login_required
def delete_record(request, slug, pk, year=None, month=None, day=None):
    habit = get_object_or_404(Habit, slug=slug)
    record = get_object_or_404(Record, pk=pk)
    user = get_object_or_404(User)
    if request.method == "POST":
        record.delete()
        return redirect(to="habit_detail", slug=habit.slug)

    return render(request, "delete_record.html", {"record": record, "habit": habit})


@login_required
def edit_record(request, slug, pk, year=None, month=None, day=None):
    habit = get_object_or_404(Habit, slug=slug)
    record = get_object_or_404(Record, pk=pk)
    user = get_object_or_404(User)
    if request.method == "POST":
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.habit_id = habit.id
            record.save()
            return redirect(
                to="record_detail",
                slug=habit.slug,
                pk=record.pk,
                year=record.date.year,
                month=record.date.month,
                day=record.date.day,
            )
    else:
        form = RecordForm(instance=record)
    return render(
        request, "edit_record.html", {"form": form, "habit": habit, "record": record}
    )


@login_required
def record_detail(request, slug, pk, year=None, month=None, day=None):
    habit = get_object_or_404(Habit, slug=slug)
    record = get_object_or_404(Record, pk=pk)
    user = get_object_or_404(User)

    return render(request, "record_detail.html", {"habit": habit, "record": record})
