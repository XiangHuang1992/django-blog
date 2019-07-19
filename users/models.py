from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

"""User模型拓展
Django的用户认证系统提供了一个内置的User对象，用于记录用户的用户名，密码等个人信息。对于Django的内
置的User模型，主要包含: username, password, email, first_name, last_name.但是对于我们自己的
实际应用来说，一个用户系统，很可能会包含其它许多字段。Django的用户系统遵循可拓展的设计原则，使得我们可以方便的拓展User模型。

拓展用户模型的两种方式：
1. 继承AbstractUser 拓展用户模型。这种方式需要迁移数据库表
2. 使用Profile模式拓展用户模型。这种方式不需要迁移数据库表。是创建一个模型来记录用户相关的数据，然后
使用一对一的方式将这个Profile模型和User关联起来。就好像每一个用户都关联着一张记录个人资料的表一样。

第二种方式和第一种方式的区别：继承AbstractUser的用户模型只有一张数据库表，而Profile这种模式有两种表，一张User模型对应的表，一张是Profile模型对应的表。两张表通过一一对应的关系相关联。这种方式在需要查询用户的profile时，需要执行额外的跨表查询操作，效率相对低一点。
"""


class Profile(models.Model):
    nickname = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    user = models.OneToOneField(User)
    objects = models.Manager()


@receiver(post_save, sender=User)
def profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.created(user=instance).save()
