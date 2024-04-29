from pyecharts import options as opts
import streamlit as st
from pyecharts.faker import Faker
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar, Line, Pie, Graph, Map, Grid

y = sorted([list(z) for z in zip(Faker.choose(), Faker.values())], reverse=True)


# == 全局色系组 ==
# fixme  饼图颜色数量应于系列长度相关
def choose_color_ulike():
    # 定义颜色方案
    color_schemes = {
        "新提色": ("#fc5d49", "#5ba3eb", "#06bb9a", "#8e7ef0", "#91CC75", "#CDA5E4", "#F5C456"),  # f4b919
        # "默认": ("#5470C6", "#91CC75", "#F5C456", "#EE6666"),  # "#73C0DE","#3BA272","#FC8452"),
        "蓝绿": ("#0072B2", "#5CB85C", "#4DA7DE", "#9BD194", "#91CC75", "#CDA5E4", "#F5C456"),
        "红橙": ("#D9534F", "#FDE74C", "#e67228", "#f9af51", "#91CC75", "#CDA5E4", "#F5C456"),
        "青黄": ("#00B8A9", "#FBC70B", "#51D2A8", "#FAD089", "#91CC75", "#CDA5E4", "#F5C456"),
        "豆青丁香": ("#8BC849", "#CDA5E4", "#6C8E37", "#A66F9D", "#91CC75", "#CDA5E4", "#F5C456"),  # 添加了深豆青色和淡丁香紫色
        "红玄": ("#EF5434", "#622A1D", "#f9800e", "#da8b8b", "#91CC75", "#CDA5E4", "#F5C456"),  # 添加了鲜黄色和灰色以增加对比
        "湖绿黛绿": ("#17EBB3", "#436567", "#D1E751", "#2C3E50", "#91CC75", "#CDA5E4", "#F5C456"),  # 添加了明亮黄绿色和深黛绿色
        "藕荷宝蓝": ("#D6B2BE", "#475EC4", "#FC6E51", "#303F9F", "#91CC75", "#CDA5E4", "#F5C456"),  # 添加了亮橙色和深宝蓝色
        "青莲杏黄": ("#7F1BAE", "#FFAA2D", "#22c5de", "#F06", "#91CC75", "#CDA5E4", "#F5C456"),  # 添加了亮蓝色和亮橙色以增加对比
    }

    with st.container():
        col_colors, col1, col2, col3, col4, col5, col6, col7, col_text, col_blank = st.columns(10)

        selected_scheme = col_colors.selectbox("显示色系", list(color_schemes.keys()))
        colors = color_schemes[selected_scheme]
        color1 = col1.color_picker("1系列", colors[0])
        color2 = col2.color_picker("2系列", colors[1])
        color3 = col3.color_picker("3系列", colors[2])
        color4 = col4.color_picker("4系列", colors[3])
        color5 = col5.color_picker("5系列", colors[4])
        color6 = col6.color_picker("6系列", colors[5])
        color7 = col7.color_picker("7系列", colors[6])

        with col_text:
            st.write("")
            st.write("")
            # st.write("当前颜色是：", (color1, color2, color3, color4))
        colors_ls = [color1, color2, color3, color4, color5, color6, color7]
    return colors_ls


def pie_base(y1_title, pie_data, colors_ls, pic_title, height):
    # 标签颜色  fixme
    pic_title = "Pie-基本图"
    p = (
        Pie()
        .add(y1_title,  # 系列名称，在鼠标移过去时的提示名称
             pie_data,  # 数据
             center=["50%", "50%"],  # 饼图位置 [距离左侧距离，距离上方距离]
             radius=["0%", "65%"],  # 中心空白圈大小，饼图缩放比例
             # rosetype="area" # # 是否显示为玫瑰图
             is_clockwise=True,  # 顺时钟排序
             is_avoid_label_overlap=True,  # 避免标签重叠
             )
        .set_series_opts(tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)", ),  # 互动提示
                         label_opts=opts.LabelOpts(formatter="{b}: {c}", ),  # 标签显示 （a系列名称 b名称 c数值 d百分比）
                         itemstyle_opts=opts.ItemStyleOpts(  # 样式设置
                             border_width=3,  # 边框宽度
                             border_color="white",  # 边框颜色 # 让边缘白色，即是视觉的间距
                             border_radius=6  # 圆角
                         ),
                         )
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),  # 「标题」
                         legend_opts=opts.LegendOpts(orient="horizontal",  # 「图例」， horizontal vertical
                                                     pos_left="25%",  # 左边距
                                                     pos_top="0%",  # 上边距
                                                     type_="scroll",  # 可滚动
                                                     ), )
        .set_colors(colors_ls)  # 色系
    )
    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(p, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")


# 「饼图缩放」及「中心圆圈调整」
def pie_radius(y1_title, pie_data, colors_ls, pic_title, height):
    c = (
        Pie()
        .add(
            y1_title,
            pie_data,
            radius=["45%", "70%"],  # 中心空白圈大小，饼图缩放比例
            center=["60%", "50%"],  # 饼图位置 [距离左侧距离，距离上方距离]
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}", ),
                         itemstyle_opts=opts.ItemStyleOpts(  # 样式设置
                             border_width=3,  # 边框宽度
                             border_color="white",  # 边框颜色 # 让边缘白色，即是视觉的间距
                             border_radius=8  # 圆角
                         ),
                         )

        .set_global_opts(
            title_opts=opts.TitleOpts(title="Pie-Radius"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
        .set_colors(colors_ls)  # 色系

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
def pie_rich_label(y1_title, pie_data, colors_ls, pic_title, height):
    pic_title = "Pie-富文本"
    p = (
        Pie()
        .add(
            y1_title,
            pie_data,
            center=["50%", "60%"],  # 饼图位置 [距离左侧距离，距离上方距离]
            radius=["35%", "57%"],  # 中心空白大小，外圈呈现大小
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
        .set_series_opts(  # label_opts=opts.LabelOpts(formatter="{b}: {c}", ),
            itemstyle_opts=opts.ItemStyleOpts(  # 样式设置
                border_width=3,  # 边框宽度
                border_color="white",  # 边框颜色 # 让边缘白色，即是视觉的间距
                border_radius=5,  # 圆角
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),
                         legend_opts=opts.LegendOpts(orient="horizontal",  # 「图例」调整， # horizontal 水平，  vertical 垂直的
                                                     pos_left="25%",  # 左边距
                                                     pos_top="0%",  # 上边距
                                                     type_="scroll",  # 可滚动，过长的图例碰到边界会自动隐藏
                                                     ),
                         )
        .set_colors(colors_ls)  # 色系
    )
    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(p, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")


# 圆环图
def pie_circle(y1_title, pie_data, colors_ls, pic_title, height):
    p = (
        Pie()
        .add(
            series_name=y1_title,
            data_pair=pie_data,
            radius=["50%", "70%"],
            label_opts=opts.LabelOpts(is_show=False, position="center"),  # 这有问题，要关掉。饼状图中间的图例名称暂时无法显示
        )

        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            label_opts=opts.LabelOpts(
                position="inside",  # 标签位置
                formatter="{d}%",  # 标签格式
                color="white",  # 标签颜色
                font_size=11,
            ),
            itemstyle_opts=opts.ItemStyleOpts(  # 样式设置
                border_width=3,  # 边框宽度
                border_color="white",  # 边框颜色 # 让边缘白色，即是视觉的间距
                border_radius=6  # 圆角
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Pie-简洁圆环"),  # 「标题」调整
            legend_opts=opts.LegendOpts(pos_left="left", pos_top="20%", orient="vertical"),
        )
        .set_colors(colors_ls)  # 色系
    )
    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(p, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")


# 双玫瑰图
def pie_rose(y1_title, pie_data, colors_ls, pic_title, height):
    pic_title = "Pie-玫瑰图"
    p = (
        Pie()
        .add(
            y1_title,
            pie_data,
            radius=["30%", "75%"],
            center=["50%", "50%"],  # 若只需要一个，这里改为 25% -> 50%,
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=True),  # 不显示标签
        )
        .set_series_opts(  # label_opts=opts.LabelOpts(formatter="{b}: {c}", ),
            itemstyle_opts=opts.ItemStyleOpts(  # 样式设置
                border_width=3,  # 边框宽度
                border_color="white",  # 边框颜色 # 让边缘白色，即是视觉的间距
                border_radius=8,  # 圆角
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=pic_title),
            legend_opts=opts.LegendOpts(orient="horizontal",  # 「图例」调整， # horizontal 水平，  vertical 垂直的
                                        pos_left="25%",  # 左边距
                                        pos_top="0%",  # 上边距
                                        type_="scroll",  # 可滚动，过长的图例碰到边界会自动隐藏
                                        ),
        )
        .set_colors(colors_ls)  # 色系
    )
    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(p, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")


# 双玫瑰图
def pie_multi_rose(y1_title, pie_data, pie2_data, colors_ls, pic_title, height):
    # 当前模板使用1个系列，若列多则需要写入其它系列参数。
    pic_title = "Pie-双玫瑰图"
    p = (
        Pie()
        # 这里加了「2个玫瑰图」，若只需要一个，注释掉第二个，把第一个的位置偏移25%改到50%即可
        .add(
            y1_title,
            pie_data,
            radius=["30%", "75%"],
            center=["25%", "50%"],  # 若只需要一个，这里改为 25% -> 50%,
            rosetype="radius",  # radius 在视觉上更清楚表现在多少。
        )
        .add(
            y1_title,
            pie2_data,
            radius=["30%", "75%"],
            center=["75%", "50%"],  # 调整饼图位置，使可以显示出两个图
            rosetype="area",
        )
        .set_series_opts(  # label_opts=opts.LabelOpts(formatter="{b}: {c}", ),
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(  # 样式设置
                border_width=3,  # 边框宽度
                border_color="white",  # 边框颜色 # 让边缘白色，即是视觉的间距
                border_radius=5,  # 圆角
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=pic_title),
            legend_opts=opts.LegendOpts(orient="horizontal",  # 「图例」调整， # horizontal 水平，  vertical 垂直的
                                        pos_left="25%",  # 左边距
                                        pos_top="0%",  # 上边距
                                        type_="scroll",  # 可滚动，过长的图例碰到边界会自动隐藏
                                        ),
        )
        .set_colors(colors_ls)  # 色系
    )
    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(p, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")


# 嵌套图
def pie_nest(y1_title, pie_data, pie2_data, colors_ls, pic_title, height):
    height = 600

    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    p = (
        Pie()
        .add(series_name=y1_title,
             data_pair=pie_data[:3],  # 部分内容
             radius=[0, "30%"],
             label_opts=opts.LabelOpts(position="inner",formatter="{b}: \n\n{d}%",color='white' ),
             )
        .add(series_name="访问来源",
             radius=["40%", "55%"],  # 这里的40%的空圈，大于上面的30%，所以视觉上看起来是嵌套图
             data_pair=pie2_data,
             label_opts=opts.LabelOpts(position="outside",
                                       formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                                       background_color="#eee",
                                       border_color="#aaa",
                                       border_width=1,
                                       border_radius=4,
                                       rich={"a": {"color": "#999", "lineHeight": 22, "align": "center"},
                                             "abg": {"backgroundColor": "#e3e3e3",
                                                     "width": "100%",
                                                     "align": "right",
                                                     "height": 22,
                                                     "borderRadius": [4, 4, 0, 0],
                                                     },
                                             "hr": {"borderColor": "#aaa",
                                                    "width": "100%",
                                                    "borderWidth": 0.5,
                                                    "height": 0,
                                                    },
                                             "b": {"fontSize": 16, "lineHeight": 33},
                                             "per": {"color": "#eee",
                                                     "backgroundColor": "#334455",
                                                     "padding": [2, 4],
                                                     "borderRadius": 2,
                                                     },
                                             },
                                       ),
             )
        .set_series_opts(  # label_opts=opts.LabelOpts(formatter="{b}: {c}", ),
            # label_opts=opts.LabelOpts(is_show=True),
            itemstyle_opts=opts.ItemStyleOpts(border_width=3,  # 边框宽度   # 样式设置
                                              border_color="white",  # 边框颜色 # 让边缘白色，即是视觉的间距
                                              border_radius=8,  # 圆角
                                              ),
            # tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)", )
        )
        .set_global_opts(legend_opts=opts.LegendOpts(pos_left="left",
                                                     orient="vertical",  # horizontal
                                                     type_="scroll",
                                                     ),
                         )
        .set_colors(colors_ls)  # 色系
    )
    grid.add(p, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")

# radius：扇区圆心角展现数据的百分比，半径展现数据的大小（用这个）
# area：所有扇区圆心角相同，仅通过半径展现数据大小（圆心相同，这个有误导）
