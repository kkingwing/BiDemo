import streamlit as st
from streamlit_echarts import st_pyecharts
import random
import pyecharts.options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType

###
# Faker库：取值和文字，方便demo图表
# Faker.choose()  # Faker.choose() 是一个「7个文本列表」
# Faker.values()  # Faker.values()是一个「7个数字的列表」
# with st.echo(code_location="below"):  # below，在执行后回显代码，above为之前
###

# ===
# 基本示例
x = Faker.choose()
y = Faker.values()
# 色系
color1 = Faker.rand_color()
color2 = None  # 确保第二个颜色与第一个不同，写个while
while color2 == color1:
    color2 = Faker.rand_color()


def bar_base():
    """基本示例"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker

    c = (
        Bar()
        .add_xaxis(x)
        .add_yaxis(series_name="商家A",  # 标题
                   y_axis=y,  # 数据
                   # color="#f46d43",  # 颜色
                   gap='1%',
                   stack="stack1",  # 若是相同的stack序号，则会堆叠
                   )
        .add_yaxis("商家B", Faker.values(), gap='1%', color=color2)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))  # is_show 标签
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"),  # 标题
                         # toolbox_opts=opts.ToolboxOpts(), # 工具箱
                         )
    )
    st_pyecharts(c)


# 百分比
def bar_percent():
    """百分比"""
    import pandas as pd

    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y1': [12, 23, 33, 3, 33],
        'y2': [3, 21, 5, 52, 43]
    })
    total_values = df['y1'] + df['y2']

    y1_percent = df['y1'] / total_values  # 计算 'y1' 的百分比
    y2_percent = df['y2'] / total_values  # 计算 'y2' 的百分比

    list_y1 = [{"value": y1, "percent": percent} for y1, percent in zip(df['y1'], y1_percent)]
    list_y2 = [{"value": y2, "percent": percent} for y2, percent in zip(df['y2'], y2_percent)]

    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.commons.utils import JsCode
    from pyecharts.globals import ThemeType
    from streamlit_echarts import st_pyecharts

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis([1, 2, 3, 4, 5])
        .add_yaxis("product1", list_y1, stack="stack1", category_gap="50%")  # category_gap 系列间隔
        .add_yaxis("product2", list_y2, stack="stack1", category_gap="50%")
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="right",
                formatter=JsCode("function(x){return Number(x.data.percent * 100).toFixed() + '%';}"),
            )
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-百分比"),  # y轴名称
                         # toolbox_opts=opts.ToolboxOpts(),
                         )
    )
    st_pyecharts(c)


# 工具箱
def bar_tool():
    """工具箱"""
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker
    import pyecharts.options as opts
    from streamlit_echarts import st_pyecharts
    from pyecharts.globals import ThemeType

    b = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis(series_name='产品A', y_axis=Faker.values(), gap='2%', color="#f46d43")  # gap，系列「间距」
        .add_yaxis(series_name='产品B', y_axis=Faker.values(), gap='2%', color=Faker.rand_color())  # color颜色设置
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-带工具箱"),  # y轴名称
                         toolbox_opts=opts.ToolboxOpts(),
                         )
    )
    st_pyecharts(b)  # , key="pyecharts", height="400px", theme=ThemeType.LIGHT)
    # st.button("Randomize data")


# 堆叠
def bar_stack():
    """堆叠"""
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker
    import pyecharts.options as opts
    from streamlit_echarts import st_pyecharts
    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values(), stack="stack1")  # stack是堆放的「组别」，相同的数字会堆叠在一起
        .add_yaxis("商家B", Faker.values(), stack="stack1")
        .add_yaxis("商家C", Faker.values(), stack="stack2")  # 有多少y轴数据依次添加
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))  # is_show 标签
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-堆叠|不显"),
            legend_opts=opts.LegendOpts(selected_map={"商家C": False}),  # 不显示某列
        )  # title是标题
        # .render("bar_stack0.html")
    )
    st_pyecharts(c)


# 自定义颜色
def bar_custom_color():
    """自定义颜色"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.commons.utils import JsCode
    from pyecharts.faker import Faker

    # 设置「产品」在「不同区间」时，显示出的颜色，该逻辑较少用。
    color_function = """
            function (params) {
                if (params.value > 0 && params.value < 50) {
                    return 'red';
                } else if (params.value > 50 && params.value < 100) {
                    return 'blue';
                }
                return 'green';
            }
            """
    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis(
            "商家A",
            Faker.values(),
            itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)),
        )
        .add_yaxis(
            "商家B",
            Faker.values(),
            itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)),
        )
        .add_yaxis(
            "商家C",
            Faker.values(),
            itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-自定义柱状颜色"))
        # .render("bar_custom_bar_color.html")
    )
    st_pyecharts(c)


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
def mix_bar_and_line():
    """组合图柱状折线"""
    import pyecharts.options as opts
    from pyecharts.charts import Bar, Line
    from pyecharts.faker import Faker
    from streamlit_echarts import st_pyecharts

    bar = (
        Bar()
        .add_xaxis(xaxis_data=Faker.months)
        # 每个y轴的数据
        ## y轴主轴第1组数据设置
        .add_yaxis(series_name="蒸发量",
                   y_axis=[round(random.uniform(1.0, 30.0), 1) for _ in range(10)],
                   label_opts=opts.LabelOpts(is_show=False),
                   )
        ## y轴主轴第2组数据设置
        .add_yaxis(series_name="降水量",
                   y_axis=[round(random.uniform(1.0, 30.0), 1) for _ in range(10)],
                   label_opts=opts.LabelOpts(is_show=False),
                   )
        ## y轴副轴数据设置
        .extend_axis(yaxis=opts.AxisOpts(name="温度",
                                         type_="value",
                                         min_=0,
                                         max_=25,
                                         interval=5,
                                         axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
                                         ))
        .set_global_opts(tooltip_opts=opts.TooltipOpts(is_show=True, trigger="axis", axis_pointer_type="cross"),
                         xaxis_opts=opts.AxisOpts(type_="category",
                                                  axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
                                                  ),
                         yaxis_opts=opts.AxisOpts(name="水量",  # y轴主轴其它设置
                                                  type_="value",
                                                  min_=0,
                                                  max_=50,  # 250, #y轴最大值， None|int
                                                  interval=10,  # 间隔
                                                  axislabel_opts=opts.LabelOpts(formatter="{value} ml"),  # 单位
                                                  axistick_opts=opts.AxisTickOpts(is_show=True),
                                                  splitline_opts=opts.SplitLineOpts(is_show=True),
                                                  ),
                         title_opts=opts.TitleOpts(title="Bar-组合图"),  # y轴名称
                         )
    )

    # 折线图其它设置
    line = (
        Line()
        .add_xaxis(xaxis_data=Faker.months)
        .add_yaxis(series_name="平均温度",
                   yaxis_index=1,
                   y_axis=[round(random.uniform(1.0, 20.0), 1) for _ in range(10)],
                   label_opts=opts.LabelOpts(is_show=False), )
    )

    st_pyecharts(bar.overlap(line))


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
def bar_mark_line_and_point():
    """标记「辅助线 & 指定点」"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker

    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        # .add_yaxis("商家B", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-辅助线 & 指定点"))
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
    )
    st_pyecharts(c)


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
def bar_days_zoom():
    """可互动选择展示日期区间"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker
    from streamlit_echarts import st_pyecharts
    from datetime import datetime, timedelta

    # 近30天日期
    days_30_list = [(datetime.today() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    c = (
        Bar()
        .add_xaxis(days_30_list)
        .add_yaxis("商家A", Faker.days_values, stack="stack1")
        # .add_yaxis("商家B", Faker.days_values,stack="stack1") # 过多花眼，不适合多字段

        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-日期区间"),
            datazoom_opts=opts.DataZoomOpts(range_start=50, range_end=100, ),  # 默认展示区间
        )
        # .render("bar_datazoom_slider.html")
    )
    st_pyecharts(c)


# 滑轮缩放
def bar_zoom():
    """滑轮可放大缩小"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker

    c = (
        Bar()
        .add_xaxis(Faker.days_attrs)
        .add_yaxis("商家A", Faker.days_values, color=Faker.rand_color())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-滑轮缩放"),
            datazoom_opts=opts.DataZoomOpts(type_="inside"),
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
        # .render("bar_datazoom_both.html")
    )
    st_pyecharts(c)


# 瀑布图
def bar_waterfall():
    """瀑布图"""
    from pyecharts.charts import Bar
    from pyecharts import options as opts

    x_data = [f"11月{str(i)}日" for i in range(1, 12)]
    y_total = [0, 900, 1245, 1530, 1376, 1376, 1511, 1689, 1856, 1495, 1292]
    y_in = [900, 345, 393, "-", "-", 135, 178, 286, "-", "-", "-"]
    y_out = ["-", "-", "-", 108, 154, "-", "-", "-", 119, 361, 203]

    c = (
        Bar()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="",
            y_axis=y_total,
            stack="总量",
            itemstyle_opts=opts.ItemStyleOpts(color="rgba(0,0,0,0)"),
        )
        .add_yaxis(series_name="收入", y_axis=y_in, stack="总量")
        .add_yaxis(series_name="支出", y_axis=y_out, stack="总量")
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(type_="value"),
            title_opts=opts.TitleOpts(title="Bar-瀑布图"),  # y轴名称
        )
        # .render("bar_waterfall_plot.html")
    )
    st_pyecharts(c)


# 条形图
def bar_reverse():
    """条形图"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker

    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-条形图"))
        # .render("bar_reversal_axis.html")
    )
    st_pyecharts(c)


# 直方图
def bar_histogram():
    """直方图"""
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.faker import Faker

    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values(), category_gap=2, color="#fdae61")
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-直方图"))
        # .render("bar_histogram.html")
    )
    st_pyecharts(c)


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
        # .render("bar_base_with_animation.html")
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
