from django import template
from ..models import Post, CateGory

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by("-create_time")[:num]


@register.simple_tag
def archives():
    return Post.objects.dates("create_time", "month", order="DESC")


@register.simple_tag
def get_categories():
    return CateGory.objects.all()
