# 根据数据库的职位信息生成图形比较薪资情况
from lagou_spider import ConnDB
from pyecharts.charts import Bar
from pyecharts import options as opts

def gen_graph():
    # 先查询数据库
    conn_info = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123qqq...A',
        'database': 'test',
        'charset': 'utf8mb4'
    }
    sql = 'select city, avg(substring_index(salary, "k", 1)) from jobs group by city;'
    conn = ConnDB(conn_info)
    results = conn.query(sql)
    
    # 生成图形
    bar = (
        Bar()
        .add_xaxis([r[0] for r in results])
        .add_yaxis("薪资", [r[1] for r in results])
        .set_global_opts(title_opts=opts.TitleOpts(title="各地区python工程师平均薪资情况"))
    )
    bar.render()


if __name__ == "__main__":
    gen_graph()
