import markdown

from django.shortcuts import get_object_or_404, render

from .models import Post, CateGory

# Create your views here.


def index(request):

    post_list = Post.objects.all().order_by("-create_time")  # 从数据库获取全部文章，按照时间最晚的排最前面
    return render(request, "index.html", context={"post_list": post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(
        post.body,
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            "markdown.extensions.toc",
        ],
    )
    return render(request, "detail.html", context={"post": post})


def archives(request, year, month):
    post_list = Post.objects.filter(
        create_time__year=year, create_time__month=month
    ).order_by("-create_time")

    return render(request, "index.html", context={"post_list": post_list})


def category(request, pk):
    cate = get_object_or_404(CateGory, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by("-create_time")

    return render(request, "index.html", context={"post_list": post_list})
