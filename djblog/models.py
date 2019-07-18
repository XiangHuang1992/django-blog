from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class CateGory(models.Model):
    """Category类
    Django要求模型必须继承models.Model类。
    Categroy 只要一个简单的分类名 name即可
    CharField指定类分类名name的数据类型。字符型。
    max_length指定了最大长度。
    Arguments:
        models {[type]} -- [description]
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)  # 文章标题
    body = models.TextField()  # 文章正文

    create_time = models.DateTimeField()  # 创建时间
    modified_time = models.DateTimeField()  # 更新时间

    excerpt = models.CharField(max_length=200, blank=True)  # 文章摘要

    category = models.ForeignKey(CateGory, on_delete=models.CASCADE)  # 文章分类
    tags = models.ManyToManyField(Tag, blank=True)  # 文章标签

    # 文章作者，直接使用了django内置的用户模型。
    # 通过外键把User和文章关联起来
    # 一篇文章只有一个作者，一个作者有多篇文章。是一对多的关系。
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("djblog:detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-create_time"]
