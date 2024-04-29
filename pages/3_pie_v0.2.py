# v 0.2 重构为「简洁模板」，去代码echo回显，
# v 0.1 基本模板。
from demo_pyecharts import bar, line, pie, graph, map  # 导入各个不同demo的图表文件， 在st里这个导入方法是正确的
import streamlit as st
import inspect
import textwrap

from streamlit_echarts import st_pyecharts
import pyecharts.options as opts
from pyecharts.charts import Bar, Line, Pie, Graph, Map, Grid
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
import pandas as pd
import random

x_series = Faker.choose()  # 数据系列
x2_series = Faker.choose()  # 数据系列
y1_series = Faker.values()
y2_series = Faker.values()
x_title = "x轴标题"
y1_title = "商家A"
y2_title = "商家B"
pic_title = "图表标题"
height = "310px"  # 图表高度

# 使用df来处理排序
df = pd.DataFrame({
    x_title: x_series,
    y1_title: y1_series,
    y2_title: y2_series,
})
# 第一个图系列数据（样例）
df_sorted = df.sort_values(by=y1_title, ascending=False)
x_series = df_sorted[x_title]
y1_series = df_sorted[y1_title]
pie_data = [list(z) for z in zip(x_series, y1_series)]

# 第二个图的系列数据（样例）
df2_sorted = df.sort_values(by=y2_title, ascending=False)
y2_series = df2_sorted[y2_title]

pie2_data= [list(z) for z in zip(x_series, y2_series)]


def main():
    with st.container(border=False):
        col1, col2, = st.columns([1, 7])
        with col1:
            with st.container(border=True):
                st.write("")
                st.button("重置模拟数据", use_container_width=True, )
                st.write("")
        with col2:
            with st.container(border=True):
                colors_ls = pie.choose_color_ulike()  # 色系组件，颜色选择器

    col1, col2, col3 = st.columns(3)
    with st.container(border=True):  # height=700,
        with col1:
            with st.container(border=True):  # height=700,
                st.write('基础图')
                pie.pie_base(y1_title, pie_data, colors_ls, pic_title, height)  # 基本图
                pie.pie_radius(y1_title, pie_data, colors_ls, pic_title, height)  # 缩放

        with col2:
            with st.container(border=True):  # height=700
                st.write('圆环图')
                pie.pie_circle(y1_title, pie_data, colors_ls, pic_title, height)  # 圆环图
                pie.pie_rich_label(y1_title, pie_data, colors_ls, pic_title, height)  # 富文本
        with col3:
            with st.container(border=True):  # height=700
                st.write('异化图')
                pie.pie_rose(y1_title, pie_data, colors_ls, pic_title, height)  # 玫瑰图
                pie.pie_multi_rose(y1_title, pie_data, pie2_data, colors_ls, pic_title, height) # 双玫瑰图

    with st.container(border=False):
        st.write('嵌套图')
        col1, col2 = st.columns([0.7, 0.35])
        with col1:
            with st.container(border=True, height=800):
                pie.pie_nest(y1_title, pie_data, pie2_data, colors_ls, pic_title, height)  # 嵌套图


if __name__ == "__main__":
    st.set_page_config(layout='wide',  # 'centered'
                       page_title="Streamlit PyECharts Demo",
                       page_icon=":chart_with_upwards_trend:"
                       )
    main()
