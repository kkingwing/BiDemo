# v 0.3 添加「数据组配色」
# v 0.2 重构为「以数据组数」为布局的模板。
# v 0.1 基本模板。
from demo_pyecharts import bar, line, pie, graph, map  # 导入各个不同demo的图表文件， 在st里这个导入方法是正确的
import streamlit as st
import inspect
import textwrap

from streamlit_echarts import st_pyecharts
import pyecharts.options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode

import pandas as pd
import random


# == 全局色系 ==
# todo 页面颜色选择器，展示与点击选择。
# todo 收集优秀配色，如「简洁app」的配色。

# # color2 = "#304656"  # green 默认绿
# color_match = [  # 色系组
#     ("#8BC849", "#CDA5E4"),  # 豆青、丁香
#     ("#EF5434", "#622A1D"),  # 红玄
#     ("#17EBB3", "#436567"),  # 湖绿、黛绿
#     ("#D6B2BE", "#475EC4"),  # 藕荷、宝蓝
#     ("#7F1BAE", "#FFAA2D"),  # 青莲、杏黄
# ]
# color1, color2 = random.choice(color_match)
# color3 = "#d14a61"  # blue ，默认蓝  blue:5470C6, green:91CC75, red:"#d14a61" , black:"#304656"

x_series = Faker.choose()  # 数据系列
y1_series = Faker.values()
y2_series = Faker.values()
y3_series = Faker.values() * 3
x_title = "x轴标题"
y1_title = "商家A"
y2_title = "商家B"
y3_title = "商家C"
pic_title = "图表标题"
height = "310px"  # 图表高度


def show_code(method):
    # 作用：显示源代码
    sourcelines, _ = inspect.getsourcelines(method)  # method是指方法名，不包含括号，如「bar」而不是「bar()」
    with st.expander("Source Code"):
        st.code(textwrap.dedent("".join(sourcelines[1:])), language="python")
    st.divider()


def main():
    st.title("Bar Demo")
    with st.container(border=False):
        col1, col2, = st.columns([1, 7])
        with col1:
            with st.container(border=True):
                st.write("")  # 占位
                st.button("重置模拟数据",use_container_width=True,)
                st.write("")  # 占位
        with col2:
            with st.container(border=True):
                color1, color2, color3, color4 = bar.choose_color_ulike()  # 色系组件，颜色选择器

    col1, col2, col3 = st.columns(3)
    with st.container(border=True):  # height=700,
        with col2:
            with st.container(border=True):  # height=700
                st.write('「两组数据」模板图')
                bar.bar_base(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title,
                             height)  # 基础图
                bar.bar_percent(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title,
                                height)  # 百分比
                bar.bar_tool(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title,
                             height)  # 工具箱
                bar.bar_reverse(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title,height)  # 条形图
                bar.bar_waterfall(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title,
                                  height)  # 瀑布图

        with col1:
            with st.container(border=True):  # height=700,
                st.write('「一组数据」模板图')
                bar.bar_mark_line_and_point(x_series, y1_title, y1_series, color1, pic_title, height)  # 特别标注
                bar.bar_days_zoom(x_series, y1_title, y1_series, color1, pic_title, height)  # 缩放+滑动日期

        with col3:
            with st.container(border=True):  # height=700,
                st.write('「三组数据」模板图')
                bar.bar_stack(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, y3_title, y3_series,
                              color3, color4, pic_title, height)  # 堆叠 & 不显
                bar.mix_bar_and_line(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, y3_title,
                                     y3_series, color3, pic_title, height)  # 组合图

                ###
                # 小众，不显示
                # bar.bar_radius()  # 改变方形柱条
                # show_code(bar.bar_radius)

                # bar.multi_y_axis()  # 多y轴
                # show_code(bar.multi_y_axis)


if __name__ == "__main__":
    st.set_page_config(layout='wide',  # 'centered'
                       page_title="Streamlit PyECharts Demo",
                       page_icon=":chart_with_upwards_trend:"
                       )
    main()

# 运行：cmd -> 「streamlit run 绝对路径」-> streamlit run D:\Code\My_project\b_变现测试\BI看板\st看板\app.py
