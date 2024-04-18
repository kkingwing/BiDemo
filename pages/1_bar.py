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
    st.title("Bar Demo")
    st.button("Randomize data")

    ###
    # 左侧菜单栏布局。 配置选择（这里暂略）
    # with st.sidebar:
    #     st.header("Configuration")
    #     selected_api = st.selectbox(label="Choose your preferred API:", options=["pyecharts", ])

    # 若要优化，改到「page」文件夹下，或是使用选择去加载，全在tab里会同时请求。
    # tab_bar, tab2, tab3 = st.tabs(["Bar", "Dog", "Owl"])
    # with tab_bar:
    col1, col2, col3 = st.columns(3)
    with st.container(border=True):  # height=700,
        with col1:
            with st.container(border=True):  # height=700,
                st.write('基础图')
                ###
                # 基础图
                bar.bar_base()  # 基本示例
                show_code(bar.bar_base)

                ###
                # 各属性

                bar.bar_percent()  # 百分比
                show_code(bar.bar_percent)

                bar.bar_stack()  # 堆叠 & 不显
                show_code(bar.bar_stack)

                ###
                # 标记「数值特征」
                # bar.bar_mark_point()  # 标记数值点
                # show_code(bar.bar_mark_point)

                # bar.bar_mark_line()  # 标记辅助线
                # show_code(bar.bar_mark_line)

                # bar.bar_custom_point()  # 标记指定数值点
                # show_code(bar.bar_custom_point)

                bar.bar_mark_line_and_point()  # 「辅助线 & 指定点」
                show_code(bar.bar_mark_line_and_point)

        with col2:
            with st.container(border=True):  # height=700
                st.write('异形图')
                ###
                # 异化
                bar.mix_bar_and_line()  # 组合图
                show_code(bar.mix_bar_and_line)

                bar.bar_histogram()  # 直方图
                show_code(bar.bar_histogram)

                bar.bar_reverse()  # 条形图
                show_code(bar.bar_reverse)

                bar.bar_waterfall()  # 瀑布图，收入支出留存
                show_code(bar.bar_waterfall)

        with col3:
            with st.container(border=True):  # height=700,
                st.write('强互动')
                bar.bar_days_zoom()  # 缩放横轴日期
                show_code(bar.bar_days_zoom)

                bar.bar_zoom()  # 滑轮缩放
                show_code(bar.bar_zoom)

                bar.zoom_data_date()  # 时间轴缩放
                show_code(bar.zoom_data_date)

                bar.bar_tool()  # 带工具箱
                show_code(bar.bar_tool)

                ###
                # 小众，不显示
                #
                # bar.bar_radius()  # 改变方形柱条
                # show_code(bar.bar_radius)
                #
                # bar.bar_custom_animation()  # 延迟动画
                # show_code(bar.bar_custom_animation)
                #
                # bar.bar_custom_color()  # 自定义颜色
                # show_code(bar.bar_custom_color)
                #
                # bar.multi_y_axis()  # 多y轴
                # show_code(bar.multi_y_axis)


if __name__ == "__main__":
    st.set_page_config(layout='wide',  # 'centered'
                       page_title="Streamlit PyECharts Demo",
                       page_icon=":chart_with_upwards_trend:"
                       )
    main()

# 运行：cmd -> 「streamlit run 绝对路径」-> streamlit run D:\Code\My_project\b_变现测试\BI看板\st看板\app.py
