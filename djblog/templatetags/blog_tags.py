from django import template
from ..models import Post, CateGory
from django.core.paginator import EmptyPage

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


@register.inclusion_tag("paginator.html", takes_context=True)
def render_paginator(context, adjacent_pages=3):
    start_page = max(context["page_obj"].number - adjacent_pages, 1)
    if start_page <= 3:
        start_page = 1
    end_page = context["page_obj"].number + adjacent_pages + 1
    if end_page >= context["paginator"].num_pages - 1:
        end_page = context["paginator"].num_pages + 1

    page_numbers = [
        n
        for n in range(start_page, end_page)
        if n in range(1, context["paginator"].num_pages + 1)
    ]

    page_obj = context["page_obj"]
    paginator = context["paginator"]

    try:
        next_ = context["page_obj"].next_page_number()
    except EmptyPage:
        next_ = None

    try:
        previous = context["page_obj"].previous_page_number()
    except EmptyPage:
        previous = None

    return {
        "page_obj": page_obj,
        "paginator": paginator,
        "page": context["page_obj"].number,
        "pages": context["paginator"].num_pages,
        "page_numbers": page_numbers,
        "next": next_,
        "previous": previous,
        "has_next": context["page_obj"].has_next(),
        "has_previous": context["page_obj"].has_previous(),
        "show_first": 1 not in page_numbers,
        "show_last": context["paginator"].num_pages not in page_numbers,
        "request": context["request"],
    }
