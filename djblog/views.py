import markdown

from django.shortcuts import get_object_or_404

from .models import Post, CateGory

from comments.forms import CommentForm

from django.views.generic import ListView, DetailView

# Create your views here.


class IndexView(ListView):
    model = Post  # 告诉Django获取的模型
    template_name = "index.html"  # 指定这个视图渲染的模版
    context_object_name = "post_list"  # 指定获取的模型列表数据保存的变量名，这个变量会传递到模版
    paginate_by = 1

    # def pagination_data(self, paginator, page, is_paginated):
    #     if not is_paginated:
    #         return {}

    #     left = []
    #     right = []

    #     left_has_more = False
    #     right_has_more = False

    #     first = False
    #     last = False
    #     page_number = page.number

    #     total_pages = paginator.num_pages
    #     page_range = paginator.page_range

    #     if page_number == 1:
    #         right = page_range[page_number:page_number + 2]

    #         if right[-1] < total_pages - 1:
    #             right_has_more = True

    #         if right[-1] < total_pages:
    #             last = True

    #     elif page_number == total_pages:
    #         left = page_range[
    #             (page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1
    #         ]

    #         if left[0] > 2:
    #             left_has_more = True

    #         if left[0] > 1:
    #             first = True

    #     else:
    #         left = page_range[
    #             (page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1
    #         ]
    #         right = page_range[page_number:page_number + 2]

    #         if right[-1] < total_pages - 1:
    #             right_has_more = True
    #         if right[-1] < total_pages:
    #             last = True

    #         if left[0] > 2:
    #             left_has_more = True
    #         if left[0] > 1:
    #             first = True

    #     data = {
    #         "left": left,
    #         "right": right,
    #         "left_has_more": left_has_more,
    #         "right_has_more": right_has_more,
    #         "first": first,
    #         "last": last,
    #     }

    #     return data

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     paginator = context.get("paginator")

    #     pagination_data = self.pagination_data(paginator, page, is_paginated)

    #     context.update(pagination_data)

    #     return context


# def index(request):

#     post_list = Post.objects.all()  # 从数据库获取全部文章，按照时间最晚的排最前面
#     return render(request, "index.html", context={"post_list": post_list})


class PostDetailView(DetailView):
    model = Post
    template_name = "detail.html"
    context_object_name = "post"

    # 复写get方法，增加阅读量统计
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        self.object.increase_views()

        return response

    # 根据id获取文章，对文章的post_body进行markdown渲染
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(
            post.body,
            extensions=[
                "markdown.extensions.extra",
                "markdown.extensions.codehilite",
                "markdown.extensions.toc",
            ],
        )
        return post

    # 获取post下的评论
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({"form": form, "comment_list": comment_list})

        return context


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     post.increase_views()

#     post.body = markdown.markdown(
#         post.body,
#         extensions=[
#             "markdown.extensions.extra",
#             "markdown.extensions.codehilite",
#             "markdown.extensions.toc",
#         ],
#     )
#     form = CommentForm()
#     comment_list = post.comment_set.all()

#     context = {"post": post, "form": form, "comment_list": comment_list}
#     return render(request, "detail.html", context=context)


class ArchivesView(ListView):
    model = Post
    template_name = "index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")

        return (
            super(ArchivesView, self)
            .get_queryset()
            .filter(create_time__year=year, create_time__month=month)
        )


# def archives(request, year, month):
#     post_list = Post.objects.filter(create_time__year=year, create_time__month=month)

#     return render(request, "index.html", context={"post_list": post_list})


class CategoryView(ListView):
    model = Post
    template_name = "index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        cate = get_object_or_404(CateGory, pk=self.kwargs.get("pk"))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# def category(request, pk):
#     cate = get_object_or_404(CateGory, pk=pk)
#     post_list = Post.objects.filter(category=cate)

#     return render(request, "index.html", context={"post_list": post_list})
