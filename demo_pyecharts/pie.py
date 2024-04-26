from pyecharts import options as opts

from pyecharts.charts import Pie
from pyecharts.faker import Faker
from streamlit_echarts import st_pyecharts

y = sorted([list(z) for z in zip(Faker.choose(), Faker.values())], reverse=True)


def pie_base():
    c = (
        Pie()
        .add("金额",  # 系列名称，在鼠标移过去时的提示名称
             y,  # 数据
             center=["50%", "60%"],  # 饼图位置 [距离左侧距离，距离上方距离]
             radius=["0%", "60%"],  # 中心空白圈大小，饼图缩放比例
             # rosetype="area", # 是否显示为玫瑰图
             )
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本图"),  # 「标题」调整
                         legend_opts=opts.LegendOpts(orient="horizontal",  # 「图例」调整， horizontal水平，vertical垂直
                                                     pos_left="25%",  # 左边距
                                                     pos_top="0%",  # 上边距
                                                     type_="scroll",  # 可滚动，过长的图例碰到边界会自动隐藏
                                                     ), )
        .set_series_opts(tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)", ),  # 互动提示
                         label_opts=opts.LabelOpts(formatter="{b}: {c}", ),  # 标签显示 （a系列名称 b名称 c数值 d百分比）
                         )
        # 「颜色」调整. 同一色系不同深浅，取色地址 ：https://0to255.com/254,121,74。 也可设置不同色系
        # .set_colors(["#e13c01", "#fe5317", "#fe6c39", "#fe865b", "#fe865b", "#feab8e", "#ffc4af"])
    )
    st_pyecharts(c, theme='light')  # 内置的只有light和dark，其它的需要设置或安装


# 定义颜色
def pie_custom_color():
    from pyecharts import options as opts
    from pyecharts.charts import Pie
    from pyecharts.faker import Faker

    c = \
        (
            Pie()
            .add("",
                 [list(z) for z in zip(Faker.choose(), Faker.values())],  # sorted(a,reverse=True))
                 center=["45%", "50%"],  # 饼图位置 [距离左侧距离，距离上方距离]
                 radius=["0%", "65%"],  # 中心空白圈大小，饼图缩放比例
                 )
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-设置颜色"),
                             legend_opts=opts.LegendOpts(orient="vertical",  # 「图例」调整,horizontal 水平，  vertical 垂直的
                                                         pos_right="0%",  # 右边距
                                                         pos_top="20%", ),  # 上边距
                             )
            # 同一色系不同深浅，取色地址 ：https://0to255.com/254,121,74。 也可设置不同色系
            .set_colors(["#e13c01", "#fe5317", "#fe6c39", "#fe865b", "#fe865b", "#feab8e", "#ffc4af"])

            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
    st_pyecharts(c)


# 「饼图缩放」及「中心圆圈调整」
def pie_radius():
    from pyecharts import options as opts
    from pyecharts.charts import Pie
    from pyecharts.faker import Faker

    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(Faker.choose(), Faker.values())],
            radius=["30%", "80%"],  # 中心空白圈大小，饼图缩放比例
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Pie-Radius"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        # .render("pie_radius.html")
    )
    st_pyecharts(c)


# 位置偏移
def pie_position():
    """调整饼图位置"""
    from pyecharts import options as opts
    from pyecharts.charts import Pie
    from pyecharts.faker import Faker

    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(Faker.choose(), Faker.values())],
            center=["40%", "50%"],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Pie-调整位置"),
            legend_opts=opts.LegendOpts(pos_left="70%"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        # .render("pie_position.html")
    )
    st_pyecharts(c)


# 图例滚动
def pie_scroll_legend():
    """滚动长图例"""
    from pyecharts import options as opts
    from pyecharts.charts import Pie
    from pyecharts.faker import Faker

    c = (
        Pie()
        .add(
            "",
            [
                list(z)
                for z in zip(
                Faker.choose() + Faker.choose() + Faker.choose(),
                Faker.values() + Faker.values() + Faker.values(),
            )
            ],
            center=["40%", "50%"],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Pie-Legend 滚动"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        # .render("pie_scroll_legend.html")
    )
    st_pyecharts(c)


# 富文本
def pie_rich_label():
    from pyecharts import options as opts
    from pyecharts.charts import Pie
    from pyecharts.faker import Faker

    c = (
        Pie()
        .add(
            "金额",
            [list(z) for z in zip(Faker.choose(), Faker.values())],
            center=["50%", "60%"],  # 饼图位置 [距离左侧距离，距离上方距离]
            radius=["40%", "55%"],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}   ",  # 富文本格式
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [2, 2, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 11, "lineHeight": 25},  # 文字大小，外框高度
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-富文本"),
                         legend_opts=opts.LegendOpts(orient="horizontal",  # 「图例」调整， # horizontal 水平，  vertical 垂直的
                                                     pos_left="25%",  # 左边距
                                                     pos_top="0%",  # 上边距
                                                     type_="scroll",  # 可滚动，过长的图例碰到边界会自动隐藏
                                                     ),
                         )
        # .render("pie_rich_label.html")
    )
    st_pyecharts(c)


# 圆环图
def pie_circle():
    """圆环图"""
    import pyecharts.options as opts
    from pyecharts.charts import Pie

    x_data = ["直接访问", "邮件营销", "联盟广告", "视频广告", "搜索引擎"]
    y_data = [335, 310, 234, 135, 1548]

    c = (
        Pie()
        .add(
            series_name="访问来源",
            data_pair=[list(z) for z in zip(x_data, y_data)],
            radius=["50%", "70%"],
            label_opts=opts.LabelOpts(is_show=False, position="center"),  # 这有问题，要关掉。饼状图中间的图例名称暂时无法显示
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Pie-简洁圆环"),  # 「标题」调整
            legend_opts=opts.LegendOpts(pos_left="left", pos_top="10%", orient="vertical"))
        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            label_opts=opts.LabelOpts(formatter="{b}: {c}")
        )
        # .render("doughnut_chart.html")
    )
    st_pyecharts(c)


# 双玫瑰图
def pie_rose():
    from pyecharts import options as opts
    from pyecharts.charts import Pie
    from pyecharts.faker import Faker

    v = Faker.choose()
    # series_data = Faker.values()
    c = (
        Pie()

        # 这里加了「2个玫瑰图」，若只需要一个，注释掉第二个，把第一个的位置偏移25%改到50%即可
        .add(
            "",
            [list(z) for z in zip(v, Faker.values())],
            radius=["30%", "75%"],
            center=["50%", "50%"],  # 若只需要一个，这里改为 25% -> 50%,
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=True),  # 不显示标签
        )

        .set_global_opts(
            title_opts=opts.TitleOpts(title="Pie-玫瑰图"),
            legend_opts=opts.LegendOpts(orient="horizontal",  # 「图例」调整， # horizontal 水平，  vertical 垂直的
                                        pos_left="25%",  # 左边距
                                        pos_top="0%",  # 上边距
                                        type_="scroll",  # 可滚动，过长的图例碰到边界会自动隐藏
                                        ),
        )
    )
    st_pyecharts(c)


# 双玫瑰图
def pie_multi_rose():
    from pyecharts import options as opts
    from pyecharts.charts import Pie
    from pyecharts.faker import Faker

    v = Faker.choose()
    # series_data = Faker.values()
    c = (
        Pie()

        # 这里加了「2个玫瑰图」，若只需要一个，注释掉第二个，把第一个的位置偏移25%改到50%即可
        .add(
            "",
            [list(z) for z in zip(v, Faker.values())],
            radius=["30%", "75%"],
            center=["25%", "50%"],  # 若只需要一个，这里改为 25% -> 50%,
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=False),  # 不显示标签
        )
        .add(
            "",
            [list(z) for z in zip(v, Faker.values())],
            radius=["30%", "75%"],
            center=["75%", "50%"],  # 调整饼图位置，使可以显示出两个图
            rosetype="area",
            # label_opts=opts.LabelOpts(is_show=False),  # 不显示标签
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Pie-玫瑰图"),
            legend_opts=opts.LegendOpts(orient="horizontal",  # 「图例」调整， # horizontal 水平，  vertical 垂直的
                                        pos_left="25%",  # 左边距
                                        pos_top="0%",  # 上边距
                                        type_="scroll",  # 可滚动，过长的图例碰到边界会自动隐藏
                                        ),
        )
    )
    st_pyecharts(c)


# 嵌套图
def pie_nest():
    import pyecharts.options as opts
    from pyecharts.charts import Pie

    inner_x_data = ["直达", "营销广告", "搜索引擎"]
    inner_y_data = [335, 679, 1548]
    inner_data_pair = [list(z) for z in zip(inner_x_data, inner_y_data)]

    outer_x_data = ["直达", "营销广告", "搜索引擎", "邮件营销", "联盟广告", "视频广告", "百度", "谷歌", "必应", "其他"]
    outer_y_data = [335, 310, 234, 135, 1048, 251, 147, 102]
    outer_data_pair = [list(z) for z in zip(outer_x_data, outer_y_data)]

    c = (
        Pie()
        .add(
            series_name="访问来源",
            data_pair=inner_data_pair,
            radius=[0, "30%"],
            label_opts=opts.LabelOpts(position="inner"),
        )
        .add(
            series_name="访问来源",
            radius=["40%", "55%"],  # 这里的40%的空圈，大于上面的30%，所以视觉上看起来是嵌套图
            data_pair=outer_data_pair,
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(
                pos_left="left",
                orient="vertical",  # horizontal
                type_="scroll",
            )
        )
        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            )
        )
        # .render("nested_pies.html")
    )
    st_pyecharts(c, height="600px")
