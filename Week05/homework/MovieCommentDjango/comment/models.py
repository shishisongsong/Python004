from django.db import models

# Create your models here.


# 电影表
class Film(models.Model):
    # id字段自动创建
    name = models.CharField(max_length=50, verbose_name="电影名称")


# 电影评论表
class Comment(models.Model):
    # id字段自动创建
    short = models.TextField(verbose_name="短评内容")
    star = models.IntegerField(verbose_name="星级")
    comment_time = models.DateField(verbose_name="短评时间")
    film = models.ForeignKey('Film', on_delete=models.CASCADE)
