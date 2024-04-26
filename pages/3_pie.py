import streamlit as st
from demo_pyecharts import bar, line, pie, graph, map  # 导入各个不同demo的图表文件， 在st里这个导入方法是正确的

import inspect
import textwrap


def show_code(method):
    # 作用：显示源代码
    sourcelines, _ = inspect.getsourcelines(method)  # method是指方法名，不包含括号，如「bar」而不是「bar()」
    with st.expander("Source Code"):
        st.code(textwrap.dedent("".join(sourcelines[1:])), language="python")
    st.divider()


def main():
    st.title("Pie Demo")
    st.button("Randomize data")

    ###
    # 左侧菜单栏布局。 配置选择（这里暂略）
    # with st.sidebar:
    #     st.header("Configuration")
    #     selected_api = st.selectbox(label="Choose your preferred API:", options=["pyecharts", ])

    col1, col2, col3 = st.columns(3)
    with st.container(border=True):  # height=700,
        with col1:
            with st.container(border=True):  # height=700,
                st.write('基础图')

                pie.pie_base()  # 基本图
                show_code(pie.pie_base)

                pie.pie_custom_color()  # 定义颜色
                show_code(pie.pie_custom_color)

                # pie.pie_position()  # 调整位置
                # show_code(pie.pie_position)

                # pie.pie_radius()  # 缩放
                # show_code(pie.pie_radius)

                # pie.pie_scroll_legend()  # 图例滚动
                # show_code(pie.pie_scroll_legend)

        with col2:
            with st.container(border=True):  # height=700
                st.write('圆环图')

                pie.pie_circle()  # 圆环图
                show_code(pie.pie_circle)

                pie.pie_rich_label()  # 富文本
                show_code(pie.pie_rich_label)

        with col3:
            with st.container(border=True):  # height=700
                st.write('异化图')

                pie.pie_rose()  # 玫瑰图
                show_code(pie.pie_rose)

                pie.pie_multi_rose()  # 双玫瑰图
                show_code(pie.pie_multi_rose)

    with st.container(border=False):
        st.write('嵌套图')
        col1, col2 = st.columns([0.7, 0.35])
        with col1:
            with st.container(border=True, height=800):
                pie.pie_nest()  # 嵌套图
                show_code(pie.pie_nest)


if __name__ == "__main__":
    st.set_page_config(layout='wide',  # 'centered'
                       page_title="Streamlit PyECharts Demo",
                       page_icon=":chart_with_upwards_trend:"
                       )
    main()
