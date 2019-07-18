from django.urls import path

from . import views

app_name = "djblog"

urlpatterns = [
    path("", views.index, name="首页"),
    path("post/<int:pk>", views.detail, name="detail"),
]
