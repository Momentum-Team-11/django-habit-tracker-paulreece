"""habit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from habitapp import views as habit_views

urlpatterns = [
    path("admin", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("accounts", include("registration.backends.simple.urls")),
    path("", habit_views.base_login, name="base_login"),
    path("home", habit_views.homepage, name="homepage"),
    path("<int:pk>/add/", habit_views.add_habit, name="add_habit"),
    path("<slug:slug>", habit_views.habit_detail, name="habit_detail"),
    path("<slug:slug>/edit", habit_views.edit_habit, name="edit_habit"),
    path("<slug:slug>/delete", habit_views.delete_habit, name="delete_habit"),
    path("<slug:slug>/add", habit_views.add_record, name="add_record"),
    path(
        "<slug:slug>/<int:pk>/<int:year>/<int:month>/<int:day>/delete",
        habit_views.delete_record,
        name="delete_record",
    ),
    path(
        "<slug:slug>/<int:pk>/<int:year>/<int:month>/<int:day>/edit",
        habit_views.edit_record,
        name="edit_record",
    ),
    path(
        "<slug:slug>/<int:pk>/<int:year>/<int:month>/<int:day>/",
        habit_views.record_detail,
        name="record_detail",
    ),
]
