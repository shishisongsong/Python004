from django.shortcuts import render

# Create your views here.
from .models import *


# 显示电影三星以上评论的全部内容
def index(request):
    film_name = Film.objects.get(id=1).name  # 电影名称
    comments = Comment.objects.filter(star__gt=3)  # 三星以上的短评内容
    return render(request, 'index.html', locals())


# 通过搜索框的关键字展示相关短评内容
def search(request):
    film_name = Film.objects.get(id=1).name  # 电影名称
    keyword = request.GET['q']  # 搜索的关键字
    comments = Comment.objects.filter(short__contains=keyword)  # 关键字相关的短评内容
    return render(request, 'index.html', locals())
