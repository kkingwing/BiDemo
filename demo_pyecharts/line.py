import streamlit as st
import pyecharts.options as opts

from pyecharts.charts import Line, Grid
from pyecharts.faker import Faker
from streamlit_echarts import st_pyecharts
import random

# 注：x数据需要是字符串，若是数值，会标点错位。
x, y = Faker.choose(), Faker.values()  ## === 常量： x y 数据源


# 基本图（含所有常使用的参数）
def line_base():
    # 定义要绘制的详细内容
    l = (  # 以下这种每换行的写法是「链式调用」，每次运行完都会返回自身，实际是 l.line()  l.add_xaxis(x)  ……
        Line()  # === 图表类型
        .add_xaxis(x)  # === x轴
        .add_yaxis(series_name="商家A",  # === y轴  # 系列名称
                   y_axis=y,  # 数据
                   color="#d14a61",  # 红色。 对这个数据系列都使用这个颜色，包括：线条、标记、图例等。
                   # areastyle_opts=opts.AreaStyleOpts(opacity=0.1),  # 面积图， opacity 不透视明度
                   # is_smooth=True, # 曲线
                   label_opts=opts.LabelOpts(is_show=False),  # 标签. 下方系列生效，其它系列不生效要其设置为False
                   # linestyle_opts=opts.LineStyleOpts(width=1),  # 「y轴线条不包含标点」的设置，一般不用，color="green"
                   # is_connect_nones=True,  # 跳过null空点连接
                   # is_symbol_show = False, # 是否显示标记点
                   # is_step = True, # 阶梯样式
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(name="最小值", type_="min"),  # 数据特征->标点
                                                           opts.MarkPointItem(name="最大值", type_="max"),
                                                           # opts.MarkPointItem(name="平均值",ttype_="average")
                                                           # opts.MarkPointItem(name="指定", coord=[x[2], y[2]], value=y[2])
                                                           ], ),
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(name="平均线", type_="average"),  # 数据特征->标线
                                                         # opts.MarkLineItem(name="最小线",type_="min"),
                                                         # opts.MarkLineItem(name="最大线",type_="max"),
                                                         # opts.MarkLineItem(name="自定义线", y=100),
                                                         ], ),

                   )
        .add_yaxis("商家B",  # 第2条y数据，参数参考上方参数。
                   Faker.values(),
                   color="#6e9ef1",  # 蓝色。
                   label_opts=opts.LabelOpts(is_show=False),
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(name="最小值", type_="min"),
                                                           opts.MarkPointItem(name="最大值", type_="max")]),
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(name="平均线", type_="average")]),
                   )
        # .add_yaxis("商家C", Faker.values())   # 若有其它「数据系列」则依次添加
        # .add_yaxis("商家D", Faker.values())
        # .add_yaxis("商家E", Faker.values())
        # .add_yaxis("商家F", Faker.values())

        .set_series_opts(label_opts=opts.LabelOpts(is_show=False),  # 标签。 「方法：「所有数据系列」的统一设置，会覆盖上方的系列内的设置
                         # areastyle_opts=opts.AreaStyleOpts(opacity=0.3),  # 面积图，不透视明度，
                         )

        # 全局设置，会覆盖上面的参数设置。
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本图"),  # 标题。 「方法： 全局设置」
                         legend_opts=opts.LegendOpts(type_="scroll",  # 图例 -> 过长图例可滚动
                                                     orient="horizontal",  # 「图例」调整， # horizontal 水平，  vertical 垂直的
                                                     selected_map={"商家B": False,  # 将某数据系列不显示
                                                                   "商家C": False,
                                                                   "商家D": False,
                                                                   "商家E": False,
                                                                   "商家F": False,
                                                                   },
                                                     pos_left=None,  # 左边距，默认居中。 "35%"
                                                     pos_top=None,  # 上边距  "0%"
                                                     ),
                         xaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True),  # 是否显示「轴线条」
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # 去x轴网格线
                                                  axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                                                  # 面积图是否「贴靠到轴」
                                                  boundary_gap=True,  # 中间点于「轴还是中间」,True在网格中间
                                                  is_show=True,  # x轴的轴身是否显示
                                                  min_=0,  # x轴最小值，只在数值时起效   # 注意，横轴不能是数值，只能是字符串构成
                                                  # max_=10, # x轴最大值
                                                  offset=10,  # 轴数值偏移
                                                  name="品类",  # x轴名称
                                                  ),
                         yaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True, ),  # 是否显示「轴线条」
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # 去y轴网格线
                                                  # type_="log",  # 设置为「对数轴」
                                                  # is_show=True,  # y轴的轴身是否显示
                                                  # min_=30, # y轴最小值，起始点非0
                                                  # max_=200, # y轴最大值
                                                  name="金额",  # y轴轴标题
                                                  axislabel_opts=opts.LabelOpts(formatter="{value}亿"),  # y轴标签格式单位
                                                  ),
                         # 互动提示，其它图表的参数一致可用。
                         tooltip_opts=opts.TooltipOpts(trigger="axis",  # 鼠标移动时显示两轴标签
                                                       axis_pointer_type="cross",
                                                       formatter="{b} {c}亿",  # 互动提示
                                                       ),

                         )
    )

    # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid = Grid()
    grid.add(l, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))

    st_pyecharts(chart=grid,
                 height="300px",  # 图表高度
                 theme="light",  # 主题色 （上面在「数据系列」定义的细节好颜色后，这里一般不使用，这里写light不生效。）另一色系是dark
                 width="100%",  # 这个是全显示的意思， 不是缩放，一般不变。
                 )


# 面积图
def line_simple_area():
    c = (
        Line()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5), is_smooth=True)  # 加圆滑参数
        .add_yaxis("商家B", Faker.values(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))

        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),  # 不显示标签
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Line-面积图"),
            # xaxis_opts=opts.AxisOpts(  # 附着两边，取消与y轴的空隙
            #     axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            #     is_scale=False,
            #     boundary_gap=False, )
        )
        # .render("line_area_style.html")
    )
    st_pyecharts(c)


# 圆弧面积图
def line_area():
    import pyecharts.options as opts
    from pyecharts.charts import Line
    from pyecharts.faker import Faker

    l = (
        Line()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values(), is_smooth=True)
        .add_yaxis("商家B", Faker.values(), is_smooth=True)
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Line-圆弧面积图"),
            xaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                is_scale=False,
                boundary_gap=False,
            ),
        )
        # .render("line_areastyle_boundary_gap.html")
    )
    st_pyecharts(l)


# 雨量图
def line_rain():
    x_data = Faker.days_attrs  # x轴显示
    y_data_rain_fall_amount = Faker.days_values  # y轴 雨流量
    y_data_flow_amount = Faker.days_values  # y轴 承接量

    l = (
        Line()
        # x、y轴数据
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="雨流量",
            y_axis=y_data_rain_fall_amount,
            yaxis_index=1,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            linestyle_opts=opts.LineStyleOpts(),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="承接量",
            y_axis=y_data_flow_amount,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            linestyle_opts=opts.LineStyleOpts(),
            label_opts=opts.LabelOpts(is_show=False),
        )
        # 副y轴
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="雨流量",  # 副y轴名称
                name_location="start",
                type_="value",
                max_=max(y_data_flow_amount),  # 5
                is_inverse=True,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),

            ),
        )

        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="承接量图",
                # subtitle="数据来自西安兰特水电测控技术有限公司",
                pos_left="center",
                pos_top="top",
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="left"),
            datazoom_opts=[
                opts.DataZoomOpts(range_start=0, range_end=100),
                opts.DataZoomOpts(type_="inside", range_start=0, range_end=10),  # max(y_data_flow_amount)
            ],
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(name="降雨量", type_="value", max_=max(y_data_flow_amount)),
        )
        .set_series_opts(
            markarea_opts=opts.MarkAreaOpts(
                is_silent=False,
                data=[
                    opts.MarkAreaItem(
                        name="承接量",
                        x=("2024/01/01-7:00", "2024/07/01-7:00"),
                        label_opts=opts.LabelOpts(is_show=False),
                        itemstyle_opts=opts.ItemStyleOpts(color="#DCA3A2", opacity=0.5),
                    ),
                    opts.MarkAreaItem(
                        name="降雨量",
                        x=("2024/01/01-7:00", "2024/07/01-7:00"),
                        label_opts=opts.LabelOpts(is_show=False),
                        itemstyle_opts=opts.ItemStyleOpts(color="#A1A9AF", opacity=0.5),
                    ),
                ],
            ),
            axisline_opts=opts.AxisLineOpts(),
        )
        # .render("rainfall.html")
    )
    st_pyecharts(l)


# 双x轴
def line_2_x_axis():
    import pyecharts.options as opts
    from pyecharts.charts import Line

    # 将在 v1.1.0 中更改
    from pyecharts.commons.utils import JsCode

    """
    Gallery 使用 pyecharts 1.0.0
    参考地址: https://echarts.apache.org/examples/editor.html?c=multiple-x-axis

    目前无法实现的功能:

    1、暂无
    """

    js_formatter = """function (params) {
            console.log(params);
            return '降水量  ' + params.value + (params.seriesData.length ? '：' + params.seriesData[0].data : '');
        }"""

    l = (
        Line()
        .add_xaxis(
            xaxis_data=["2016-1", "2016-2", "2016-3", "2016-4", "2016-5", "2016-6", "2016-7", "2016-8", "2016-9",
                        "2016-10", "2016-11", "2016-12"], )
        .extend_axis(
            xaxis_data=["2015-1", "2015-2", "2015-3", "2015-4", "2015-5", "2015-6", "2015-7", "2015-8", "2015-9",
                        "2015-10", "2015-11", "2015-12"],
            xaxis=opts.AxisOpts(
                type_="category",
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                axisline_opts=opts.AxisLineOpts(
                    is_on_zero=False, linestyle_opts=opts.LineStyleOpts(color="#6e9ef1")
                ),
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True, label=opts.LabelOpts(formatter=JsCode(js_formatter))
                ),
            ),
        )
        .add_yaxis(
            series_name="2015 降水量",
            is_smooth=True,
            symbol="emptyCircle",
            is_symbol_show=False,
            # xaxis_index=1,
            color="#d14a61",
            y_axis=[2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
        .add_yaxis(
            series_name="2016 降水量",
            is_smooth=True,
            symbol="emptyCircle",
            is_symbol_show=False,
            color="#6e9ef1",
            y_axis=[3.9, 5.9, 11.1, 18.7, 48.3, 69.2, 231.6, 46.6, 55.4, 18.4, 10.3, 0.7],
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Line-双x轴"),
            legend_opts=opts.LegendOpts(),
            tooltip_opts=opts.TooltipOpts(trigger="none", axis_pointer_type="cross"),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                axisline_opts=opts.AxisLineOpts(
                    is_on_zero=False, linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True, label=opts.LabelOpts(formatter=JsCode(js_formatter))
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            ),
        )
        # .render("multiple_x_axes.html")
    )
    st_pyecharts(l)


# 阶梯图
def line_step():
    import pyecharts.options as opts
    from pyecharts.charts import Line
    from pyecharts.faker import Faker

    x_data = [a + 1 for a in range(0, 12)]  # 生成12个月份的数字当轴， 这里有点问题
    y_data = [b + random.randint(1, 10) for b in range(0, 12)]  # 这里要使用的是一个累计数据，
    l = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis("商家A", y_data, is_step=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-阶梯图"))
        # .render("line_step.html")
    )
    st_pyecharts(l)


# 标记点及辅助线
def line_mark_point_line():
    import pyecharts.options as opts
    from pyecharts.charts import Line
    from pyecharts.faker import Faker

    x, y = Faker.choose(), Faker.values()
    l = (
        Line()
        .add_xaxis(x)
        .add_yaxis(
            "商家A",
            y,
            markpoint_opts=opts.MarkPointOpts(
                data=[opts.MarkPointItem(name="指定标点", coord=[x[2], y[2]], value=y[2])]
            ),
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]), color='#111111',
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-标记点线"))
        # .render("line_markpoint_custom.html")
    )
    st_pyecharts(l)


# 标记点-数据特征
def line_mark_points():
    import pyecharts.options as opts
    from pyecharts.charts import Line
    from pyecharts.faker import Faker

    c = (
        Line()
        .add_xaxis(Faker.choose())
        .add_yaxis(
            "商家A",
            Faker.values(),
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min")]),
        )
        .add_yaxis(
            "商家B",
            Faker.values(),
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-最大小值"))
        # .render("line_markpoint.html")
    )
    st_pyecharts(c)


# 标记辅助线
def line_mark_line():
    import pyecharts.options as opts
    from pyecharts.charts import Line
    from pyecharts.faker import Faker

    c = (
        Line()
        .add_xaxis(Faker.choose())
        .add_yaxis(
            "商家A",
            Faker.values(),
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
        )
        .add_yaxis(
            "商家B",
            Faker.values(),
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-MarkLine"))
        # .render("line_markline.html")
    )
    st_pyecharts(c)


# 标记区域
def line_mark_area():
    x_data = [
        "00:00", "01:15", "02:30", "03:45", "05:00",
        "06:15", "07:30", "08:45", "10:00", "11:15",
        "12:30", "13:45", "15:00", "16:15", "17:30",
        "18:45", "20:00", "21:15", "22:30", "23:45"
    ]

    y_data = [
        300, 280, 250, 260, 270,
        300, 550, 500, 400, 390,
        380, 390, 400, 500, 600,
        750, 800, 700, 600, 400
    ]

    l = (
        Line()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="用电量",
            y_axis=y_data,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Line-分区段"),  # , subtitle="纯属虚构"
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            xaxis_opts=opts.AxisOpts(boundary_gap=False),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value} W"),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,
                dimension=0,
                pieces=[
                    {"lte": 6, "color": "green"},
                    {"gt": 6, "lte": 8, "color": "red"},  # 范围，颜色
                    {"gt": 8, "lte": 14, "color": "green"},
                    {"gt": 14, "lte": 17, "color": "red"},
                    {"gt": 17, "color": "green"},
                ],
            ),
        )
        .set_series_opts(
            markarea_opts=opts.MarkAreaOpts(
                data=[
                    opts.MarkAreaItem(name="早高峰", x=("07:30", "10:00")),
                    opts.MarkAreaItem(name="晚高峰", x=("17:30", "21:15")),
                ]
            )
        )
        # .render("distribution_of_electricity.html")
    )
    st_pyecharts(l)


def line_stype():
    import pyecharts.options as opts
    from pyecharts.charts import Line
    from pyecharts.faker import Faker

    l = (
        Line()
        .add_xaxis(xaxis_data=Faker.choose())
        .add_yaxis(
            "商家A",
            Faker.values(),
            symbol="triangle",
            symbol_size=20,
            linestyle_opts=opts.LineStyleOpts(color="green", width=4, type_="dashed"),
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=3, border_color="yellow", color="blue"
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-样式设置"))
        # .render("line_itemstyle.html")
    )

    st_pyecharts(l)


# 堆叠区域图
def line_stack_area():
    # 这里是总数
    import pyecharts.options as opts
    from pyecharts.charts import Line

    x_data = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    y_data = [820, 932, 901, 934, 1290, 1330, 1320]

    l = (
        Line()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="邮件营销",
            stack="总量",
            y_axis=[120, 132, 101, 134, 90, 230, 210],
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="联盟广告",
            stack="总量",
            y_axis=[220, 182, 191, 234, 290, 330, 310],
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="视频广告",
            stack="总量",
            y_axis=[150, 232, 201, 154, 190, 330, 410],
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="直接访问",
            stack="总量",
            y_axis=[320, 332, 301, 334, 390, 330, 320],
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="搜索引擎",
            stack="总量",
            y_axis=[820, 932, 901, 934, 1290, 1330, 1320],
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=True, position="top"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Line-堆积图"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
        # .render("stacked_area_chart.html")
    )
    st_pyecharts(l)
