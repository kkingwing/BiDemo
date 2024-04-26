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
y1_series = Faker.values()
y2_series = Faker.values()
y3_series = Faker.values() * 3
x_title = "x轴标题"
y1_title = "商家A"
y2_title = "商家B"
y3_title = "商家C"
pic_title = "图表标题"
height = "310px"  # 图表高度

def main():
    st.title("Line Demo")
    with st.container(border=False):
        col1, col2, = st.columns([1, 7])
        with col1:
            with st.container(border=True):
                st.write("")
                st.button("重置模拟数据",use_container_width=True,)
                st.write("")
        with col2:
            with st.container(border=True):
                color1, color2, color3, color4 = bar.choose_color_ulike()  # 色系组件，颜色选择器


    col1, col2, col3 = st.columns(3)
    with st.container(border=True):  # height=700,
        with col1:
            with st.container(border=True):  # height=700,
                st.write('1组数据图')
                line.line_base(x_series, y1_title, y1_series, color1, y2_title, y2_series, color2, pic_title, height)  # 基本示例
                line.line_mark_point_line(x_series, y1_title, y1_series, color1, pic_title, height)  # 标记点
                line.line_step()  # 阶梯图
                line.line_stype()  # 风格设置 ，「虚线、数据点」样式
                line.line_mark_area()  # 区域分段
                # line.line_basic_area()  # 基本面积
                # line.line_area()  # 圆弧面积图


        with col2:
            with st.container(border=True):  # height=700
                st.write('2组数据图')

                line.line_2_x_axis()  # 双x轴
                line.line_simple_area()  # 面积图


        with col3:
            with st.container(border=True):  # height=700,
                st.write('3组数据图')

                line.line_rain()  # 雨量图

                line.line_stack_area()  # 堆积图


if __name__ == "__main__":
    st.set_page_config(layout='wide',  # 'centered'
                       page_title="Streamlit PyECharts Demo",
                       page_icon=":chart_with_upwards_trend:"
                       )
    main()
