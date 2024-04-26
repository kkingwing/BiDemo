# v0.13 增加「颜色选择器」
# v0.13 填加可用「鼠标滚动缩放」，清理部分不再使用的功能。
# v0.11 所有图基本模板，
import streamlit as st
from streamlit_echarts import st_pyecharts

import pyecharts.options as opts
from pyecharts.charts import Bar, Line
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode

import pandas as pd
from datetime import datetime, timedelta
import random


###
# Faker库：取值和文字，方便demo图表
# Faker.choose()  # Faker.choose() 是一个「7个文本列表」
# Faker.values()  # Faker.values()是一个「7个数字的列表」
# with st.echo(code_location="below"):  # below，在执行后回显代码，above为之前
###

# == 全局色系组 ==
# todo 收集优秀配色，如「简洁app」的配色。「islider」的配色。
def choose_color_ulike():
    # 定义颜色方案
    color_schemes = {
        "新提色": ("#fc5d49", "#5ba3eb", "#06bb9a", "#8e7ef0"),  # f4b919
        "默认": ("#5470C6", "#91CC75", "#F5C456", "#EE6666"),  # "#73C0DE","#3BA272","#FC8452"
        "蓝绿": ("#0072B2", "#5CB85C", "#4DA7DE", "#9BD194"),
        "红橙": ("#D9534F", "#FDE74C", "#e67228", "#f9af51"),
        "青黄": ("#00B8A9", "#FBC70B", "#51D2A8", "#FAD089"),
        "豆青丁香": ("#8BC849", "#CDA5E4", "#6C8E37", "#A66F9D"),  # 添加了深豆青色和淡丁香紫色
        "红玄": ("#EF5434", "#622A1D", "#f9800e", "#da8b8b"),  # 添加了鲜黄色和灰色以增加对比
        "湖绿黛绿": ("#17EBB3", "#436567", "#D1E751", "#2C3E50"),  # 添加了明亮黄绿色和深黛绿色
        "藕荷宝蓝": ("#D6B2BE", "#475EC4", "#FC6E51", "#303F9F"),  # 添加了亮橙色和深宝蓝色
        "青莲杏黄": ("#7F1BAE", "#FFAA2D", "#22c5de", "#F06"),  # 添加了亮蓝色和亮橙色以增加对比
    }

    with st.container():
        col_colors, col1, col2, col3, col4, col_text, col_blank = st.columns([5, 1, 1, 1, 1, 10, 1])

        selected_scheme = col_colors.selectbox("显示色系", list(color_schemes.keys()))
        colors = color_schemes[selected_scheme]
        color1 = col1.color_picker("1系列", colors[0])
        color2 = col2.color_picker("2系列", colors[1])
        color3 = col3.color_picker("3系列", colors[2])
        color4 = col4.color_picker("4系列", colors[3])
        with col_text:
            st.write("")
            st.write("")
            st.write("当前颜色是：", (color1, color2, color3, color4))
    return color1, color2, color3, color4


"#5470C6", "#91CC75", "#F5C456", "#EE6666", "#73C0DE", "#3BA272", "#FC8452",


# # 数据系列
# x_series = Faker.choose()
# y1_series = Faker.values()
# y2_series = Faker.values()
# x_title = "x轴标题"
# y1_title = "商家A"
# y2_title = "商家B"
# pic_title = "图表标题"
# # 图表高度
# height = "350px"


def bar_base(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title, height):
    """基本示例"""
    pic_title = "基础图"
    c = (
        Bar()
        .add_xaxis(x_series)
        .add_yaxis(series_name=y1_title,  # 标题
                   y_axis=y1_series,  # 数据
                   color=color1,  # 颜色
                   gap='1%',  # 组间距
                   stack="stack1",  # 若是相同的stack序号，则会堆叠
                   )
        .add_yaxis(y2_title, y2_series, gap='1%', color=color2)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))  # is_show 标签
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title, ),
                         datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
                         )
    )
    st_pyecharts(c, height=height, width="100%")


# 百分比
def bar_percent(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title, height):
    pic_title = "百分比"
    """百分比"""
    # 使用df来运行计算
    df = pd.DataFrame({'x': x_series,
                       'y1': y1_series,
                       'y2': y2_series,
                       })
    total_values = df['y1'] + df['y2']
    y1_percent = df['y1'] / total_values  # 计算 'y1' 的百分比
    y2_percent = df['y2'] / total_values  # 计算 'y2' 的百分比
    list_y1 = [{"value": y1, "percent": percent} for y1, percent in zip(df['y1'], y1_percent)]
    list_y2 = [{"value": y2, "percent": percent} for y2, percent in zip(df['y2'], y2_percent)]

    c = (
        Bar()  # init_opts=opts.InitOpts(theme=ThemeType.LIGHT)
        .add_xaxis(x_series)
        .add_yaxis(series_name=y1_title,
                   y_axis=list_y1,
                   color=color1,  # 颜色
                   stack="stack1",
                   category_gap="50%",  # 柱条之间的间隔
                   )
        .add_yaxis(series_name=y2_title,
                   y_axis=list_y2,
                   color=color2,
                   stack="stack1",
                   category_gap="50%",
                   )
        .set_series_opts(label_opts=opts.LabelOpts(position="right",
                                                   formatter=JsCode(
                                                       "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"),
                                                   ))
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),
                         datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
                         )
    )
    st_pyecharts(c, height=height, width="100%")


# 工具箱
def bar_tool(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title, height):
    pic_title = "工具箱"
    """工具箱"""
    c = (
        Bar()
        .add_xaxis(x_series)
        .add_yaxis(series_name=y1_title, y_axis=y1_series, gap='2%', color=color1)  # gap，系列「间距」
        .add_yaxis(series_name=y2_title, y_axis=y2_series, gap='2%', color=color2)  # color颜色设置
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),  # y轴名称
                         toolbox_opts=opts.ToolboxOpts(),  # 工具箱
                         datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
                         )
    )
    st_pyecharts(c, height=height, width="100%")


# 多y轴
def multi_y_axis():
    """多y轴"""
    import pyecharts.options as opts
    from pyecharts.charts import Bar, Line

    colors = ["#5793f3", "#d14a61", "#675bba"]
    x_data = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    legend_list = ["蒸发量", "降水量", "平均温度"]
    evaporation_capacity = [
        2.0,
        4.9,
        7.0,
        23.2,
        25.6,
        76.7,
        135.6,
        162.2,
        32.6,
        20.0,
        6.4,
        3.3,
    ]
    rainfall_capacity = [
        2.6,
        5.9,
        9.0,
        26.4,
        28.7,
        70.7,
        175.6,
        182.2,
        48.7,
        18.8,
        6.0,
        2.3,
    ]
    average_temperature = [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2]

    bar = (
        Bar(init_opts=opts.InitOpts())  # width="1280px", height="720px")
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="蒸发量", y_axis=evaporation_capacity, yaxis_index=0, color=colors[1]
        )
        .add_yaxis(
            series_name="降水量", y_axis=rainfall_capacity, yaxis_index=1, color=colors[0]
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="蒸发量",
                type_="value",
                min_=0,
                max_=250,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=colors[1])
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="温度",
                min_=0,
                max_=25,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=colors[2])
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name="降水量",
                min_=0,
                max_=250,
                position="right",
                offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=colors[0])
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            title_opts=opts.TitleOpts(title="Bar-多y轴"),  # y轴名称
        )
    )

    line = (
        Line()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="平均温度", y_axis=average_temperature, yaxis_index=2, color=colors[2]
        )
    )

    # bar.overlap(line).render("multiple_y_axes.html")
    st_pyecharts(bar.overlap(line), width="600px", height="400px")


# 组合图
def mix_bar_and_line(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, y3_title, y3_series,
                     color3, pic_title, height):
    pic_title = "组合图"
    """组合图柱状折线"""
    bar = (
        Bar()
        .add_xaxis(xaxis_data=x_series)
        .add_yaxis(series_name=y1_title,  ## y轴主轴第1组数据设置
                   y_axis=y1_series,
                   color=color1,
                   # label_opts=opts.LabelOpts(is_show=False),
                   )
        .add_yaxis(series_name=y2_title,  ## y轴主轴第2组数据设置
                   y_axis=y2_series,
                   color=color2,
                   # label_opts=opts.LabelOpts(is_show=False),
                   )
        ## y轴副轴数据设置
        .extend_axis(yaxis=opts.AxisOpts(name=y3_title,
                                         type_="value",
                                         # min_=0,
                                         # max_=25,
                                         # interval=5,
                                         # axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
                                         ))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(tooltip_opts=opts.TooltipOpts(is_show=True, trigger="axis", axis_pointer_type="cross"),
                         xaxis_opts=opts.AxisOpts(type_="category",
                                                  axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
                                                  ),
                         # yaxis_opts=opts.AxisOpts(name="水量",  # y轴主轴其它设置
                         #                          type_="value",
                         #                          min_=0,
                         #                          max_=50,  # 250, #y轴最大值， None|int
                         #                          interval=10,  # 间隔
                         #                          axislabel_opts=opts.LabelOpts(formatter="{value} ml"),  # 单位
                         #                          axistick_opts=opts.AxisTickOpts(is_show=True),
                         #                          splitline_opts=opts.SplitLineOpts(is_show=True),
                         #                          ),
                         title_opts=opts.TitleOpts(title=pic_title),  # y轴名称
                         datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
                         )
    )

    # 折线图其它设置
    line = (
        Line()
        .add_xaxis(xaxis_data=x_series)
        .add_yaxis(series_name="平均温度",
                   yaxis_index=1,
                   color=color3,
                   y_axis=y3_series,
                   label_opts=opts.LabelOpts(is_show=False), )
    )

    st_pyecharts(bar.overlap(line), height=height, width="100%")


# 标记数值点
def bar_mark_point():
    """标记数值点"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker
    from streamlit_echarts import st_pyecharts

    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-数值特征"))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                    opts.MarkPointItem(type_="average", name="平均值"),
                ]
            ),
        )
        # .render("bar_markpoint_type.html")
    )
    st_pyecharts(c)


# 标记「辅助线 & 指定点」
def bar_mark_line_and_point(x_series, y1_title, y1_series, color1, pic_title, height):
    """标记「辅助线 & 指定点」"""
    pic_title = "特别标注"
    c = (
        Bar()
        .add_xaxis(x_series)
        .add_yaxis(y1_title, y1_series, color=color1)
        # .add_yaxis("商家B", Faker.values())

        .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                         markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="平均值"),
                                                               # opts.MarkLineItem(type_="min", name="最小值"),
                                                               # opts.MarkLineItem(type_="max", name="最大值"),
                                                               ]),
                         markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="最大值"),
                                                                 opts.MarkPointItem(type_="min", name="最小值"),
                                                                 # opts.MarkPointItem(type_="average", name="平均值"),
                                                                 ]),
                         )
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),
                         datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
                         )
    )
    st_pyecharts(c, height=height, width="100%")


# 标记指定数值点
def bar_custom_point():
    """标记自定义数值点"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker

    x, y = Faker.choose(), Faker.values()
    c = (
        Bar()
        .add_xaxis(x)
        .add_yaxis(
            "商家A",
            y,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(name="自定义标记点", coord=[x[2], y[2]], value=y[2]),
                    opts.MarkPointItem(name="自定义标记点", coord=[x[3], y[3]], value=y[3]),
                ]  # 索引从0开始
            ),
        )
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-指定点标记"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        # .render("bar_markpoint_custom.html")
    )
    st_pyecharts(c)


# 标记自定义辅助线
def custom_mark_line():
    """标记自定义辅助线"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker

    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-辅助线"))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(y=50, name="yAxis=50")]
            ),
        )
        # .render("bar_markline_custom.html")
    )
    st_pyecharts(c)


# 改变方形柱条
def bar_radius():
    """改变方形柱条"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.commons.utils import JsCode
    from pyecharts.faker import Faker

    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values(), category_gap="60%")
        .set_series_opts(
            itemstyle_opts={
                "normal": {
                    "color": JsCode(
                        """new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 244, 255, 1)'
                }, {
                    offset: 1,
                    color: 'rgba(0, 77, 167, 1)'
                }], false)"""
                    ),
                    "barBorderRadius": [30, 30, 30, 30],
                    "shadowColor": "rgb(0, 160, 221)",
                }
            }
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-渐变圆柱"))
        # .render("bar_border_radius.html")
    )
    st_pyecharts(c, )


# 可互动选择展示日期区间
def bar_days_zoom(x_series, y1_title, y1_series, color1, pic_title, height):
    """可互动选择展示日期区间"""
    pic_title = "滑动日期"
    x_series = [(datetime.today() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
    y1_series = [random.randint(1, 100) for i in range(30)]
    c = (
        Bar()
        .add_xaxis(x_series)
        .add_yaxis(y1_title, y1_series, stack="stack1", color=color1)
        # .add_yaxis("商家B", Faker.days_values,stack="stack1") # 过多花眼，不适合多字段
        .set_global_opts(
            title_opts=opts.TitleOpts(title=pic_title),
            # datazoom_opts=opts.DataZoomOpts(range_start=50, range_end=100, ),  # 默认展示区间
            datazoom_opts=[opts.DataZoomOpts(range_start=50, range_end=100, ),  # 「日期区间」滑动
                           opts.DataZoomOpts(type_="inside")],  # 数据区域可缩放
        )
    )
    st_pyecharts(c, height=height, width="100%")


# 滚轮缩放
def bar_zoom():  # x_series,  y1_title, y1_series, pic_title, height
    """滑轮可放大缩小"""
    pic_title = "滚轮缩放"
    x_series = [(datetime.today() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
    y1_series = [random.randint(1, 100) for i in range(30)]
    c = (
        Bar()
        .add_xaxis(x_series)
        .add_yaxis("商家A", y1_series, color=color1)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=pic_title),
            datazoom_opts=opts.DataZoomOpts(type_="inside"),  # 滚轮缩放
        )
        # .render("bar_datazoom_inside.html")
    )
    st_pyecharts(c)


# 可互动鼠标滑轮可放大缩小&带时间轴
def zoom_data_date():
    """带时间轴缩放"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker

    c = (
        Bar()
        .add_xaxis(Faker.days_attrs)
        .add_yaxis("商家A", Faker.days_values, color=Faker.rand_color())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-时间轴缩放"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )
    st_pyecharts(c)


# 瀑布图
def bar_waterfall(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title, height):
    pic_title = "Bar-瀑布图"
    """瀑布图"""
    # x_data = [f"11月{str(i)}日" for i in range(1, 12)]
    x_series = [(datetime.today() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 12)]

    # y1_series 流入 ，y2_series 流出
    y1_series = [900, 345, 393, "-", "-", 135, 178, 286, "-", "-", "-"]
    y2_series = ["-", "-", "-", 108, 154, "-", "-", "-", 119, 361, 203]
    y1_series = [0 if val == "-" else val for val in y1_series]
    y2_series = [0 if val == "-" else val for val in y2_series]

    # y_total = [0, 900, 1245, 1530, 1376, 1376, 1511, 1689, 1856, 1495, 1292]

    y_total = [0]
    # y_total = [y1_series[0]]  # 计算 y_total
    for i in range(1, len(y1_series)):
        y_total.append(y_total[i - 1] + y1_series[i - 1] - y2_series[i - 1])

    c = (
        Bar()
        .add_xaxis(xaxis_data=x_series)
        .add_yaxis(
            series_name="",
            y_axis=y_total,
            stack="总量",
            itemstyle_opts=opts.ItemStyleOpts(color="rgba(0,0,0,0)"),
        )
        .add_yaxis(series_name=y1_title, y_axis=y1_series, color=color1, stack="总量")
        .add_yaxis(series_name=y2_title, y_axis=y2_series, color=color2, stack="总量")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False), )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(type_="value"),
            title_opts=opts.TitleOpts(title=pic_title),  # y轴名称
            datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
        )
    )
    st_pyecharts(c, height=height, width="100%")


# 条形图
def bar_reverse(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title, height):
    pic_title = "Bar-条形图"
    """条形图"""
    c = (
        Bar()
        .add_xaxis(x_series)
        .add_yaxis(y1_title, y1_series)
        .add_yaxis(y2_title, y2_series)
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),
                         )
    )
    st_pyecharts(c, height=height * 2, width="100%")


# 直方图
def bar_histogram(x_series, y1_title, y1_series, color1, pic_title, height):
    pic_title = "直方图"
    """直方图"""
    c = (
        Bar()
        .add_xaxis(x_series)
        .add_yaxis(y1_title, y1_series, category_gap=0, color="#fdae61")
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title))
    )
    st_pyecharts(c, height=height, width="100%")


# 堆叠
def bar_stack(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, y3_title, y3_series,
              color3, color4, pic_title, height):
    pic_title = "堆叠&不显"
    y4_title = "不显"
    """堆叠"""
    c = (
        Bar()
        .add_xaxis(x_series)
        .add_yaxis(y1_title, y1_series, color=color1, stack="stack1")  # stack是堆放的「组别」，相同的数字会堆叠在一起
        .add_yaxis(y2_title, y2_series, color=color2, stack="stack1")
        .add_yaxis(y3_title, y3_series, color=color3, stack="stack2")  # 有多少y轴数据依次添加
        .add_yaxis(y4_title, y3_series, color=color4, stack="stack3")  # 有多少y轴数据依次添加
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))  # is_show 标签
        .set_global_opts(
            title_opts=opts.TitleOpts(title=pic_title),
            legend_opts=opts.LegendOpts(selected_map={y4_title: False}),  # 不显示某列
            datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
        )  # title是标题
    )
    st_pyecharts(c, height=height, width="100%")


# 延迟动画
def bar_custom_animation():
    """延迟出现-入场动画"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker

    c = (
        Bar(
            init_opts=opts.InitOpts(
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="elasticOut"
                )
            )
        )
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-延迟动画", subtitle="我是副标题"))
    )
    st_pyecharts(c)

# ===
# """绘制api
# def st_pyecharts(
#     chart: Base
#     theme: Union[str, Dict]   # ThemeType.LIGHT, ThemeType.DARK. 其它实测不支持
#     events: Dict[str, str]
#     height: int
#     width: str
#     renderer: str
#     map: Map
#     key: str
# )
# """
# ===
