"""
URLs for the course delete app.
"""
from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^delete-course$', views.delete_course, name="delete_course"),
]