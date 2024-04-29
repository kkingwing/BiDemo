# v 0.2 重构为「简洁模板」。
# v 0.1 基本模板。
import streamlit as st
import pyecharts.options as opts

from pyecharts.charts import Line, Grid
from pyecharts.faker import Faker
from streamlit_echarts import st_pyecharts
import random
from pyecharts.commons.utils import JsCode

# 注：x数据需要是字符串，若是数值，会标点错位。
x, y = Faker.choose(), Faker.values()  ## === 常量： x y 数据源


# 单线基本图
def line_single_base(x_series, y1_title, y1_series, color1, pic_title, height):
    pic_title = "Line-基本图"
    # 定义要绘制的详细内容
    l = (  # 以下这种每换行的写法是「链式调用」，每次运行完都会返回自身，实际是 l.line()  l.add_xaxis(x)  ……
        Line()  # === 图表类型
        .add_xaxis(x_series)  # === x轴
        .add_yaxis(series_name=y1_title,  # === y轴  # 系列名称
                   y_axis=y1_series,  # 数据
                   color=color1,  # "#d14a61",  # 红色。 对这个数据系列都使用这个颜色，包括：线条、标记、图例等。
                   # areastyle_opts=opts.AreaStyleOpts(opacity=0.1),  # 面积图， opacity 不透视明度
                   # is_smooth=True, # 曲线
                   # label_opts=opts.LabelOpts(is_show=False),  # 标签. 下方系列生效，其它系列不生效要其设置为False
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
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False),  # 标签。 「方法：「所有数据系列」的统一设置，会覆盖上方的系列内的设置
                         # areastyle_opts=opts.AreaStyleOpts(opacity=0.3),  # 面积的不透视明度，
                         )

        # 全局设置，会覆盖上面的参数设置。
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),  # 标题。 「方法： 全局设置」
                         legend_opts=opts.LegendOpts(type_="scroll",  # 图例 -> 过长图例可滚动
                                                     orient="horizontal",  # 「图例」调整， # horizontal 水平，  vertical 垂直的
                                                     # selected_map={"商家B": False,  # 将某数据系列不显示
                                                     #               },
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
                                                  # axislabel_opts=opts.LabelOpts(formatter="{value}"),  # y轴标签格式单位
                                                  ),
                         # 互动提示，其它图表的参数一致可用。
                         tooltip_opts=opts.TooltipOpts(trigger="axis",  # 鼠标移动时显示两轴标签
                                                       axis_pointer_type="cross",
                                                       # formatter="{b} {c}",  # 互动提示 # 增加这个的互动效果差
                                                       ),
                         datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
                         )
    )

    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(l, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")


# 基本面积图
def line_area(x_series, y1_title, y1_series, color1, pic_title, height):
    pic_title = "Line-基本面积图"
    l = (
        Line()
        .add_xaxis(x_series)
        .add_yaxis(y1_title, y1_series, color=color1,
                   areastyle_opts=opts.AreaStyleOpts(opacity=0.1),  # 面积图， opacity 不透视明度
                   is_smooth=False,  # 曲线
                   label_opts=opts.LabelOpts(is_show=True),  #
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(name="最小值", type_="min"),  # 数据特征->标点
                                                           opts.MarkPointItem(name="最大值", type_="max"),
                                                           ], ),
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(name="平均线", type_="average"),  # 数据特征->标线
                                                         ], ),
                   )
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=pic_title),
            xaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True),  # 是否显示「轴线条」
                                     splitline_opts=opts.SplitLineOpts(is_show=False),  # 去x轴网格线
                                     axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                                     boundary_gap=False,  # 是否x第1个贴靠在y轴上开始。
                                     is_show=True,  # x轴的轴身是否显示
                                     offset=10,  # 轴数值偏移
                                     name="品类",  # x轴名称
                                     ),
            yaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True, ),  # 是否显示「轴线条」
                                     splitline_opts=opts.SplitLineOpts(is_show=False),  # 去y轴网格线
                                     name="金额",  # y轴轴标题
                                     ),
            # 互动提示，提示最大小值，取消注释可显示值内容而非最大小值。
            tooltip_opts=opts.TooltipOpts(trigger="axis",  # item，axis # 鼠标移动时显示两轴标签
                                          trigger_on="mousemove",
                                          axis_pointer_type="cross",
                                          # formatter="{b} {c}",  # 互动提示 # 增加这个的互动效果差
                                          ),
            datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
        )
    )
    grid = Grid() # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(l, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")


# 双线基本图（含所有常使用的参数）
def line_base(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title, height):
    pic_title = "Line-隐藏数据"
    # 定义要绘制的详细内容
    l = (  # 以下这种每换行的写法是「链式调用」，每次运行完都会返回自身，实际是 l.line()  l.add_xaxis(x)  ……
        Line()  # === 图表类型
        .add_xaxis(x_series)  # === x轴
        .add_yaxis(series_name=y1_title,  # === y轴  # 系列名称
                   y_axis=y1_series,  # 数据
                   color=color1,  # "#d14a61",  # 红色。 对这个数据系列都使用这个颜色，包括：线条、标记、图例等。
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
        .add_yaxis(y2_title,  # 第2条y数据，参数参考上方参数。
                   y2_series,
                   color=color2,  # "#6e9ef1",  # 蓝色。
                   label_opts=opts.LabelOpts(is_show=False),
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(name="最小值", type_="min"),
                                                           opts.MarkPointItem(name="最大值", type_="max")]),
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(name="平均线", type_="average")]),
                   )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False),  # 标签。 「方法：「所有数据系列」的统一设置，会覆盖上方的系列内的设置
                         # areastyle_opts=opts.AreaStyleOpts(opacity=0.3),  # 面积图，不透视明度，
                         )

        # 全局设置，会覆盖上面的参数设置。
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),  # 标题。 「方法： 全局设置」
                         legend_opts=opts.LegendOpts(type_="scroll",  # 图例 -> 过长图例可滚动
                                                     orient="horizontal",  # 「图例」调整， # horizontal 水平，  vertical 垂直的
                                                     selected_map={"商家A": False,  # 将某数据系列不显示
                                                                   "商家C": False,
                                                                   },
                                                     pos_left=None,  # 左边距，默认居中。 "35%"
                                                     pos_top=None,  # 上边距  "0%"
                                                     ),
                         xaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True),  # 是否显示「轴线条」
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # 去x轴网格线
                                                  axistick_opts=opts.AxisTickOpts(is_align_with_label=True),  # 是否「贴靠到轴」
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
                                                  # axislabel_opts=opts.LabelOpts(formatter="{value}"),  # y轴标签格式单位
                                                  ),
                         # 互动提示，其它图表的参数一致可用。
                         tooltip_opts=opts.TooltipOpts(trigger="axis",  # 鼠标移动时显示两轴标签
                                                       axis_pointer_type="cross",
                                                       # formatter="{b} {c}",  # 互动提示
                                                       ),
                         datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
                         )
    )
    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(l, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")


# 面积图
def line_simple_area(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title, height):
    pic_title = "Line-面积图"
    l = (
        Line()
        .add_xaxis(x_series)
        .add_yaxis(y1_title, y1_series, color=color1, is_smooth=True, )
        .add_yaxis(y2_title, y2_series, color=color2, is_smooth=True, )
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1),  # 不透视度
            label_opts=opts.LabelOpts(is_show=False),  # 不显示标签
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),  # 标题。 「方法： 全局设置」
                         xaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True),  # 是否显示「轴线条」
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # 去x轴网格线
                                                  axistick_opts=opts.AxisTickOpts(is_align_with_label=False, ),
                                                  boundary_gap=False,  # 中间点于「轴还是中间」,True在网格中间
                                                  is_show=True,  # x轴的轴身是否显示
                                                  name="品类",  # x轴名称
                                                  ),
                         yaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True, ),  # 是否显示「轴线条」
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # 去y轴网格线
                                                  # type_="log",  # 设置为「对数轴」
                                                  # is_show=True,  # y轴的轴身是否显示
                                                  # min_=30, # y轴最小值，起始点非0
                                                  # max_=200, # y轴最大值
                                                  name="金额",  # y轴轴标题
                                                  # axislabel_opts=opts.LabelOpts(formatter="{value}"),  # y轴标签格式单位
                                                  ),
                         # 互动提示，其它图表的参数一致可用。
                         tooltip_opts=opts.TooltipOpts(trigger="axis",  # 鼠标移动时显示两轴标签
                                                       axis_pointer_type="cross",
                                                       # formatter="{b} {c}",  # 互动提示
                                                       ),
                         datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
                         )
    )
    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(l, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")


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
def line_2_x_axis(x_series, x2_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title, height):
    pic_title = "Line-双x轴"
    x_series = ["2016-1", "2016-2", "2016-3", "2016-4", "2016-5", "2016-6", "2016-7", ]
    x2_series = ["2015-1", "2015-2", "2015-3", "2015-4", "2015-5", "2015-6", "2015-7", ]
    l = (
        Line()
        .add_xaxis(xaxis_data=x_series, )
        .extend_axis(xaxis_data=x2_series,
                     xaxis=opts.AxisOpts(
                         type_="category",
                         axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                         axisline_opts=opts.AxisLineOpts(is_on_zero=False,
                                                         linestyle_opts=opts.LineStyleOpts(color=color2)),  # "#6e9ef1"
                         axispointer_opts=opts.AxisPointerOpts(is_show=True,
                                                               # label=opts.LabelOpts(formatter=JsCode(js_formatter))
                                                               ), ),
                     )
        .add_yaxis(series_name=y1_title,
                   y_axis=y1_series,
                   color=color1,  # "#d14a61",
                   is_smooth=True,
                   # symbol="emptyCircle", # 默认即是圆点，不需要再说明。
                   is_symbol_show=False,  # 标点(不显示）
                   label_opts=opts.LabelOpts(is_show=True, color=color1),  # 标签显示
                   linestyle_opts=opts.LineStyleOpts(width=2),  # 线条粗
                   )
        .add_yaxis(series_name=y2_title,
                   y_axis=y2_series,
                   color=color2,
                   is_smooth=True,
                   # symbol="emptyCircle", # 默认即是圆点，不需要再说明。
                   is_symbol_show=False,
                   label_opts=opts.LabelOpts(is_show=True, color=color2),  # 标签显示
                   linestyle_opts=opts.LineStyleOpts(width=2),  # 线条粗
                   )
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),
                         # legend_opts=opts.LegendOpts(),
                         tooltip_opts=opts.TooltipOpts(trigger="none", axis_pointer_type="cross"),
                         xaxis_opts=opts.AxisOpts(type_="category",
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # 去x轴网格线
                                                  axisline_opts=opts.AxisLineOpts(is_on_zero=True,
                                                                                  linestyle_opts=opts.LineStyleOpts(
                                                                                      color=color1)),
                                                  axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                                                  axispointer_opts=opts.AxisPointerOpts(is_show=True),
                                                  ),
                         yaxis_opts=opts.AxisOpts(type_="value",
                                                  splitline_opts=opts.SplitLineOpts(
                                                      is_show=False,  # y轴网格线
                                                      linestyle_opts=opts.LineStyleOpts(opacity=1)),
                                                  ),
                         datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
                         )
    )
    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(l, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")


# 阶梯图
def line_step(x_series, y1_title, y1_series, color1, pic_title, height):
    x_series = [str(a + 1) + "月" for a in range(0, 12)]  # 生成12个月份的数字当轴， 这里有点问题
    y1_series = [b + random.randint(1, 10) for b in range(0, 12)]  # 这里要使用的是一个累计数据，
    pic_title = "Line-阶梯图"
    l = (
        Line()
        .add_xaxis(x_series)
        .add_yaxis(y1_title, y1_series, color=color1, is_step=True)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False),  # 标签。 「方法：「所有数据系列」的统一设置，会覆盖上方的系列内的设置
                         # areastyle_opts=opts.AreaStyleOpts(opacity=0.3),  # 面积图，不透视明度，
                         )

        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),  # 标题。 「方法： 全局设置」
                         # legend_opts=opts.LegendOpts(type_="scroll",  # 图例 -> 过长图例可滚动
                         #                             orient="horizontal",  # 「图例」调整， # horizontal 水平，  vertical 垂直的
                         #                             # selected_map={"商家B": False,  # 将某数据系列不显示
                         #                             #               },
                         #                             pos_left=None,  # 左边距，默认居中。 "35%"
                         #                             pos_top=None,  # 上边距  "0%"
                         #                             ),
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
                                                  # axislabel_opts=opts.LabelOpts(formatter="{value}"),  # y轴标签格式单位
                                                  ),
                         # 互动提示，其它图表的参数一致可用。
                         tooltip_opts=opts.TooltipOpts(trigger="axis",  # 鼠标移动时显示两轴标签
                                                       axis_pointer_type="cross",
                                                       # formatter="{b} {c}",  # 互动提示 # 增加这个的互动效果差
                                                       ),
                         datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
                         )
    )

    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(l, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")


# 标记点及辅助线
def line_mark_point_line(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title, height):
    # x, y = Faker.choose(), Faker.values()
    l = (
        Line()
        .add_xaxis(x_series)
        .add_yaxis(
            y1_title,
            y1_series,
            color=color1,
            markpoint_opts=opts.MarkPointOpts(
                data=[opts.MarkPointItem(name="指定标点", coord=[x[2], y[2]], value=y[2])]
            ),
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),  # color='#111111',
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-标记点线"))
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


def line_stype(x_series, y1_title, y1_series, color1, pic_title, height):
    pic_title = "Line-样式设置"
    l = (
        Line()
        .add_xaxis(xaxis_data=x_series)
        .add_yaxis(
            y1_title,
            y1_series,
            symbol="triangle",
            symbol_size=10,  # 标点大小
            linestyle_opts=opts.LineStyleOpts(
                color=color1,  # color="green",
                width=2,  # 连线线宽
                curve=3,  # 曲度
                type_="dash"  # 前冲动画，solid  实线。
            ),
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=2,
                border_color=color1,  # "yellow",
                color=color1,  # "blue"
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),  # 标题。 「方法： 全局设置」
                         xaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True),  # 是否显示「轴线条」
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # 去x轴网格线
                                                  axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                                                  boundary_gap=True,  # 中间点于「轴还是中间」,True在网格中间
                                                  is_show=True,  # x轴的轴身是否显示
                                                  offset=10,  # 轴数值偏移
                                                  name="品类",  # x轴名称
                                                  ),
                         yaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True, ),  # 是否显示「轴线条」
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # 去y轴网格线
                                                  is_show=True,  # y轴的轴身是否显示
                                                  name="金额",  # y轴轴标题
                                                  ),
                         # 互动提示，其它图表的参数一致可用。
                         tooltip_opts=opts.TooltipOpts(trigger="axis",  # 鼠标移动时显示两轴标签
                                                       axis_pointer_type="cross",
                                                       # formatter="{b} {c}",  # 互动提示 # 增加这个的互动效果差
                                                       ),
                         datazoom_opts=opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),  # 滚轮缩放
                         )
    )

    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(l, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")


# 多系列-累计堆积图
def line_stack_area(x_series,
                    y1_title, y1_series, color1,
                    y2_title, y2_series, color2,
                    y3_title, y3_series, color3,
                    y4_title, y4_series, color4,
                    pic_title, height):
    pic_title = "Line-堆积图"
    l = (
        Line()
        .add_xaxis(xaxis_data=x_series)
        .add_yaxis(series_name=y1_title, y_axis=y1_series, color=color1, stack="stack1", is_symbol_show=False)
        .add_yaxis(series_name=y2_title, y_axis=y2_series, color=color2, stack="stack1", is_symbol_show=False)
        .add_yaxis(series_name=y3_title, y_axis=y3_series, color=color3, stack="stack1", is_symbol_show=False)
        .add_yaxis(series_name=y4_title, y_axis=y4_series, color=color4, stack="stack1", is_symbol_show=False)
        .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.1),  # 不透视度
                         label_opts=opts.LabelOpts(is_show=False),  # 不显示标签
                         )
        .set_global_opts(title_opts=opts.TitleOpts(title=pic_title),
                         legend_opts=opts.LegendOpts(orient="vertical",  # 「图例」调整,horizontal 水平，  vertical 垂直的
                                                     pos_right="0%",  # 右边距
                                                     pos_top="20%",   # 上边距
                                                     selected_map={y4_title: False}  # 默认不显
                                                     ),
                         tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                         yaxis_opts=opts.AxisOpts(type_="value",
                                                  axistick_opts=opts.AxisTickOpts(is_show=True),
                                                  splitline_opts=opts.SplitLineOpts(is_show=False), ),
                         xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False,
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),
                                                  ),
                         )

    )
    grid = Grid()  # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid.add(l, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(chart=grid, height=height, width="100%")
