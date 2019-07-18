import markdown

from django.shortcuts import get_object_or_404, render

from .models import Post, CateGory

from comments.forms import CommentForm

# Create your views here.


def index(request):

    post_list = Post.objects.all()  # 从数据库获取全部文章，按照时间最晚的排最前面
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
    form = CommentForm()
    comment_list = post.comment_set.all()

    context = {"post": post, "form": form, "comment_list": comment_list}
    return render(request, "detail.html", context=context)


def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year=year, create_time__month=month)

    return render(request, "index.html", context={"post_list": post_list})


def category(request, pk):
    cate = get_object_or_404(CateGory, pk=pk)
    post_list = Post.objects.filter(category=cate)

    return render(request, "index.html", context={"post_list": post_list})
