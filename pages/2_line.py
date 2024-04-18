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
    st.title("Line Demo")
    st.button("Randomize data")

    ###
    # 左侧菜单栏布局。 配置选择（这里暂略）
    # with st.sidebar:
    #     st.header("Configuration")
    #     selected_api = st.selectbox(label="Choose your preferred API:", options=["pyecharts", ])

    # 若要优化，改到「page」文件夹下，或是使用选择去加载，全在tab里会同时请求。
    # tab_bar, tab2, tab3 = st.tabs(["Line", "Dog", "Owl"])
    # with tab_bar:
    col1, col2, col3 = st.columns(3)
    with st.container(border=True):  # height=700,
        with col1:
            with st.container(border=True):  # height=700,
                st.write('基础图')
                ###
                # 基础图
                line.line_base()  # 基本示例
                show_code(line.line_base)

                line.line_simple_area()  # 面积图，合一，注释以下。
                show_code(line.line_simple_area)

                # line.line_basic_area()  # 基本面积
                # show_code(line.line_basic_area)

                # line.line_area()  # 圆弧面积图
                # show_code(line.line_area)

                line.line_stype()  # 风格设置 ，「虚线、数据点」样式
                show_code(line.line_stype)

        with col2:
            with st.container(border=True):  # height=700
                st.write('优化图')

                line.line_2_x_axis()  # 双x轴
                show_code(line.line_2_x_axis)

                line.line_mark_point_line()  # 标记点
                show_code(line.line_mark_point_line)

                # line.line_mark_points()  # 标记数据特征点
                # show_code(line.line_mark_points)
                #
                # line.line_mark_line()  # 标记辅助线
                # show_code(line.line_mark_line)

                line.line_stack_area()  # 堆积图
                show_code(line.line_stack_area)

        with col3:
            with st.container(border=True):  # height=700,
                st.write('异形图')

                line.line_step()  # 阶梯图
                show_code(line.line_step)

                line.line_rain()  # 雨量图
                show_code(line.line_rain)

                line.line_mark_area()  # 区域分段
                show_code(line.line_mark_area)


if __name__ == "__main__":
    st.set_page_config(layout='wide',  # 'centered'
                       page_title="Streamlit PyECharts Demo",
                       page_icon=":chart_with_upwards_trend:"
                       )
    main()
