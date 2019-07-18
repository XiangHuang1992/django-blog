from django.urls import path

from . import views

app_name = "djblog"

urlpatterns = [
    path("", views.index, name="首页"),
    path("posts/<int:pk>/", views.detail, name="detail"),
]
