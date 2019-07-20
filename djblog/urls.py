from django.urls import path

from . import views
from .feeds import AllPostRssFeed

app_name = "djblog"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path(
        "archives/<int:year>/<int:month>/", views.ArchivesView.as_view(), name="archives"
    ),
    path("category/<int:pk>/", views.CategoryView.as_view(), name="category"),
    path("tag/<int:pk>/", views.TagView.as_view(), name="tag"),
    path("all/rss/", AllPostRssFeed(), name="rss"),
]
