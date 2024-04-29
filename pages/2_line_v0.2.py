# v0.2 重构为简洁模板
# v0.1 基本模板
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

x_series = Faker.choose()  # 数据系列
x2_series = Faker.choose()  # 数据系列
y1_series = Faker.values()
y2_series = Faker.values()
y3_series = Faker.values() * 3
y4_series = Faker.values() * 3
x_title = "x轴标题"
y1_title = "商家A"
y2_title = "商家B"
y3_title = "商家C"
y4_title = "商家D"
pic_title = "图表标题"
height = "310px"  # 图表高度


def main():
    st.title("Line Demo")
    with st.container(border=False):
        col1, col2, = st.columns([1, 7])
        with col1:
            with st.container(border=True):
                st.write("")
                st.button("重置模拟数据", use_container_width=True, )
                st.write("")
        with col2:
            with st.container(border=True):
                color1, color2, color3, color4 = bar.choose_color_ulike()  # 色系组件，颜色选择器

    col1, col2, col3 = st.columns(3)
    with st.container(border=True):  # height=700,
        with col1:
            with st.container(border=True):  # height=700,
                st.write('1组数据图')
                line.line_single_base(x_series, y1_title, y1_series, color1, pic_title, height)  # 基本图
                line.line_area(x_series, y1_title, y1_series, color1, pic_title, height)  # 面积图
                line.line_step(x_series, y1_title, y1_series, color1, pic_title, height)  # 阶梯图
                line.line_stype(x_series, y1_title, y1_series, color1, pic_title, height)  # 风格设置

        with col2:
            with st.container(border=True):  # height=700
                st.write('2组数据图')
                # 基本示例
                line.line_base(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title,
                               height)
                # 面积图
                line.line_simple_area(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title,
                                      height)

        with col3:
            with st.container(border=True):  # height=700,
                st.write('3组数据图')
                # 双x轴
                line.line_2_x_axis(x_series, x2_series, y1_title, y1_series, color1, y2_title, y2_series, color2,
                                   pic_title, height)
                # 多系列-累计堆积图
                line.line_stack_area(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, y3_title,
                                     y3_series, color3, y4_title, y4_series, color4, pic_title, height)


if __name__ == "__main__":
    st.set_page_config(layout='wide',  # 'centered'
                       page_title="Streamlit PyECharts Demo",
                       page_icon=":chart_with_upwards_trend:"
                       )
    main()
