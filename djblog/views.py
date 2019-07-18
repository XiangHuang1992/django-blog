from django.shortcuts import render, get_object_or_404

from .models import Post

# Create your views here.


def index(request):

    post_list = Post.objects.all().order_by("-create_time")  # 从数据库获取全部文章，按照时间最晚的排最前面
    return render(request, "index.html", context={"post_list": post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "derail.html", context={"post": post})

