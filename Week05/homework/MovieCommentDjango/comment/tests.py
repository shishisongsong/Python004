from django.test import TestCase

# Create your tests here.
from .models import Comment, Film
import pandas as pd


# 将文件的数据插入到数据库中
def insert_data():
    file_path = '/Users/chenpingan/学习/python/Demo/spide_learn/week05_test/homework/moviecomments.csv'
    
    # 数据清洗
    df = pd.read_csv(file_path)
    df.columns = ['star_str', 'comment_time', 'short']  # 添加列头
    df = df.fillna('无')  # 填充缺失值
    # 通过字典映射，添加数字星级这一列
    star_str_to_num = {
        '力荐': 5,
        '推荐': 4,
        '还行': 3,
        '较差': 2,
        '很差': 1,
        '无': 0
    }
    df['star'] = df.star_str.map(star_str_to_num)
    # 去除star_str这一列，并进行列排序
    order = ['star', 'comment_time', 'short']
    df = df[order]

    # 插入数据库
    for t in df.itertuples(name=None, index=False):
        # 通过zip将列名和数据一一映射，然后转换成字典
        # 最后通过**字典，解包为关键字参数
        film = Film.objects.get(id=1)  # 外建电影id
        Comment.objects.create(film=film, **dict(zip(order, t)))
        # c = Comment(film=film, **dict(zip(order, t)))
        # c.save(force_insert=True)


insert_data()
