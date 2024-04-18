import pyecharts.options as opts
import streamlit as st
from pyecharts.charts import Line, Bar, Pie, Grid
from streamlit_echarts import st_pyecharts
import pandas as pd
from sqlalchemy import create_engine


st.set_page_config(
    page_title='Bi-Share',  # 浏览器的标签标题，
    page_icon='🔥',  # 标签图标，支持emoji
    layout='wide',  # 主区域布局，默认为「居中的centered「，也可以选为「布满的wide」
    initial_sidebar_state='auto',
    # menu_items={  # 右上角文字链接，键为固定字符串
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    # }

)


# === 一、连接sql  ===
@st.cache_data  # 缓存装饰器 （第一次为真正读取，其后使用缓存的df）
def conn_sql_data(table_name="dw_sample_data"):
    con = st.connection("mydb", type="sql", autocommit=True)  # 本地会读取secrets.toml，云端会读取环境。
    sql = f"SELECT * FROM {table_name}"
    df = con.query(sql)
    return df


df = conn_sql_data(table_name="dw_sample_data")

# === 二、数据ETL  ===
# 1. df清洗（至ods/dw可用层级）|  截断、新增、去除、格式转换、
df = df[df['year'] == 2020]  # 截取
df.sort_values(by=["year", "sales"], ascending=[False, True], inplace=True)  # 排序
# df['月'] = df['月'].astype(str)  # 类型转换 （横轴一般需要为文本格式）

df_sizer = df.copy()  # 复制 DataFrame。
# === 三、1. 筛选器  ===
# v3 动态筛选器，与 columns元素数量相连
values_col = 'sales'
columns = ['month', 'area', 'brand', 'phonetype', 'gender', 'age_range']  # 定义要循环的标签
# 筛选器的相互限制 fixme
# 动态生成筛选器，以 columns 列表长度动态关联。
selected_values_dict = {}  # 用于收集筛选器选择的数据，遍历过滤df
num_columns = len(columns)  # 确定要使用的列数
columns_list = st.columns(num_columns)  # 使用列表收集，在下方调用。不写固定的col1,col2等
with st.container():
    for i, label in enumerate(columns):
        with columns_list[i]:  # 使用索引选择要用于此循环迭代的列
            sizer_column = sorted(df_sizer[label].unique(), reverse=False)
            selected_values = st.multiselect(label=label, options=sizer_column)
            selected_values_dict[label] = selected_values
            if selected_values:
                df_sizer = df_sizer[df_sizer[label].isin(selected_values)]

# === 三、数据提取  ===
## 1.范围筛选
df_filter = df_sizer.copy()


## 2.透视表 #fixme， 以下取值若字段筛选后无值存在，会报错， null无法 .tolist()  | 无数据处理
### 创建透视表，返回需要的数据结果
def pivot_to_lists(df, index_cols, value_col, sort_by_value=True, agg='sum'):
    """
    从DataFrame中创建透视表，并返回索引列表和值列表。

    :param df: DataFrame，输入数据集。
    :param index_cols: list of str，用于透视表索引的列名列表。
    :param value_col: str，透视表值的列名。
    :param sort_by_value: bool，默认为True。按照值列（sales）排序；如果为False，按照索引列排序（例如月份）,通常在需要按月份排序时使用。
    :param agg: str，聚合函数类型，默认为「sum」。可选值包括「mean（均值）、sum（总和）、count（计数）」。
    :return: tuple，包含索引列表和值列表。
    """
    pt = df.pivot_table(index=index_cols, values=value_col, aggfunc=agg)
    pt = pt.head(15)  # 截断，只显示透视结果的前n行数据
    if sort_by_value:
        pt.sort_values(by=value_col, ascending=True, inplace=True)
    else:
        pt.sort_index(inplace=True)
    index_ls = pt.index.tolist()
    value_ls = pt[value_col].tolist()
    return index_ls, value_ls


try:
    # 使用循环动态生成变量名，并调用函数
    for col in columns:
        # 生成变量名
        ls_name = 'ls_' + col
        ls_consume_name = 'ls_consume_' + col
        # 调用函数，生成变量
        if col == "month":  # 这里判断不要值排序的，比如当字段为月时。
            locals()[ls_name], locals()[ls_consume_name] = pivot_to_lists(df_filter, [col], values_col,
                                                                          sort_by_value=False)
        else:
            locals()[ls_name], locals()[ls_consume_name] = pivot_to_lists(df_filter, [col], values_col,
                                                                          sort_by_value=True)
        # st.write(ls_name)
except:
    st.write('所选内容数据为空。')
    pass

# ls_月, ls_consume_月 = pivot_to_lists(df_filter, ['月'], 'sales', sort_by_value=False)
# ls_品牌, ls_consume_品牌 = pivot_to_lists(df_filter, ['品牌'], 'sales')
# ls_性别, ls_consume_性别 = pivot_to_lists(df_filter, ['性别'], 'sales')
# ls_地区, ls_consume_地区 = pivot_to_lists(df_filter, ['地区'], 'sales')
# ls_型号, ls_consume_型号 = pivot_to_lists(df_filter, ['型号'], 'sales')
# ls_年龄分段, ls_consume_年龄分段 = pivot_to_lists(df_filter, ['年龄分段'], 'sales')


# 结果截取放在这个位置
# 截取（应该是一个参数） fixme
# pt_phonetype = pt_phonetype.sort_values(by='sales', ascending=False)  # 排序截取前10个，只显示这部分
# if len(pt_phonetype) >= 10:  # 过长时截取前10项
#     pt_phonetype = pt_phonetype[:10]
# pt_phonetype = pt_phonetype.sort_values(by='sales', ascending=True)  # 逆序一下


# == 全局色系 ==
color_1 = "#d14a61"  # blue ，默认蓝  blue:5470C6, green:91CC75, red:"#d14a61" , black:"#304656"
color_2 = "#304656"  # green 默认绿


# === 四、连接pyecharts  ===
def line_month(x, y, title="月度趋势"):  # 行1列1图
    # 透视表-数据
    # x = ls_month  # 传入数据
    # y = [round(x / 100000000, 2) for x in ls_consume_month]  # 除以亿
    # 创建折线图
    line = (
        Line(init_opts=opts.InitOpts(bg_color="#FFFFFF", )  # 背景色
             # animation_opts=opts.AnimationOpts(animation_delay=1000, animation_easing="elasticOut"),  # 动画延迟，
             )
        .add_xaxis(x)
        .add_yaxis("sales",
                   y,
                   color=color_1,  # 色系1。 对这个数据系列都使用这个颜色，包括：线条、标记、图例等。
                   # areastyle_opts=opts.AreaStyleOpts(opacity=0.1),  # 面积图， opacity 不透视明度
                   # is_smooth=True, # 曲线
                   label_opts=opts.LabelOpts(is_show=False, ),  # 系列数据标签. 下方系列生效，其它系列不生效要其设置为False
                   is_connect_nones=True,  # 跳过null空点连接
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(name="最小值", type_="min"),  # 数据特征->标点
                                                           opts.MarkPointItem(name="最大值", type_="max"),
                                                           ], ),
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(name="平均线", type_="average"),  # 数据特征->标线
                                                         ], ),
                   )
        .set_global_opts(title_opts=opts.TitleOpts(title=title),  # 标题。 「方法： 全局设置」
                         legend_opts=opts.LegendOpts(type_="scroll",  # 图例 -> 过长图例可滚动
                                                     orient="horizontal",  # 「图例」调整， # horizontal 水平，  vertical 垂直的
                                                     selected_map={"商家B": False,  # 将某数据系列不显示
                                                                   },
                                                     ),
                         xaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True),  # 是否显示「轴线条」
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # 去x轴网格线
                                                  axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                                                  # 面积图是否「贴靠到轴」
                                                  boundary_gap=True,  # 中间点于「轴还是中间」,True在网格中间
                                                  is_show=True,  # x轴的轴身是否显示
                                                  min_=0,  # 0  # x轴最小值，只在数值时起效
                                                  # max_=10, # x轴最大值
                                                  name="月份",  # 轴轴标题
                                                  offset=10,  # 轴数值偏移
                                                  ),
                         yaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True, ),  # 是否显示「轴线条」
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # 去y轴网格线
                                                  # type_="log",  # 设置为「对数轴」
                                                  is_show=True,  # y轴的轴身是否显示
                                                  name="金额",  # y轴轴标题
                                                  # min_=0,  # y轴最小值，起始点非0
                                                  # max_=200, # y轴最大值
                                                  # offset=-30,  # 轴数值偏移
                                                  axislabel_opts=opts.LabelOpts(formatter="{value}亿"),  # 标签格式
                                                  ),
                         tooltip_opts=opts.TooltipOpts(
                             trigger="axis", axis_pointer_type="cross", formatter="{c}亿",  # 鼠标移至时的互动提示
                         ),
                         )
    )
    # 创建网格布局，偏移边距，使轴标签可以显示完全。
    grid = Grid()
    grid.add(line, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"))
    st_pyecharts(grid, height="380px", )


def bar_brand(x, y, title):
    """条形图"""
    # x = ls_brand
    # y = [round(x / 100000000, 2) for x in ls_consume_brand]  # 除以亿

    c = (
        Bar()
        .add_xaxis(x)
        .add_yaxis(
            "sales",
            y,
            category_gap="60%",
            color=color_1,
        )
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right", formatter="{c}亿"))
        .set_global_opts(title_opts=opts.TitleOpts(title=title),  # 标题。 「方法： 全局设置」
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
                         xaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=False),  # 是否显示「轴线条」
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # 去x轴网格线
                                                  axistick_opts=opts.AxisTickOpts(is_align_with_label=True, ),
                                                  # 面积图是否「贴靠到轴」
                                                  boundary_gap=True,  # 中间点于「轴还是中间」,True在网格中间
                                                  # is_show=False,  # x轴的轴身是否显示
                                                  # min_=0,  # 0  # x轴最小值，只在数值时起效
                                                  max_=int(max(y) * 1.35),  # 条形图，x轴的最大值
                                                  # max_=10, # x轴最大值
                                                  # name="月份",  # y轴轴标题
                                                  ),
                         yaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True, ),  # 是否显示「轴线条」
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # y轴网格线
                                                  # type_="log",  # 设置为「对数轴」
                                                  # is_show=True,  # y轴的轴身是否显示
                                                  # min_=0,  # y轴最小值，起始点非0
                                                  # max_=int(max(ls_consume_brand) * 1.2),  # ,200, # y轴最大值
                                                  name="金额",  # y轴轴标题
                                                  ),
                         tooltip_opts=opts.TooltipOpts(trigger="axis",
                                                       axis_pointer_type="cross",
                                                       formatter="{b} {c}亿"
                                                       ),  # 鼠标移动时显示两轴标签
                         )
    )

    st_pyecharts(c, height="755px", )


def pie_sex(x, y, title="性别占比"):
    # x = ls_gender
    # y = [round(x / 100000000, 2) for x in ls_consume_gender]  # 除以亿
    data = sorted([list(z) for z in zip(x, y)], reverse=True)
    c = (
        Pie()

        .add("金额",  # 系列名称，在鼠标移过去时的提示名称
             data,  # 数据
             center=["50%", "50%"],  # 饼图位置 [距离左侧距离，距离上方距离]
             radius=["40%", "55%"],  # 中心空白圈大小，饼图缩放比例
             # rosetype="area", # 是否显示为玫瑰图
             )
        .set_global_opts(title_opts=opts.TitleOpts(title=title),  # 「标题」调整
                         legend_opts=opts.LegendOpts(orient="horizontal",  # 「图例」调整， horizontal水平，vertical垂直
                                                     pos_left="40%",  # 左边距
                                                     pos_top="5%",  # 上边距
                                                     type_="scroll",  # 可滚动，过长的图例碰到边界会自动隐藏
                                                     ), )
        .set_series_opts(tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c}亿 ({d}%)", ),  # 提示
                         label_opts=opts.LabelOpts(formatter="{b}: {d}%", ),  # 直接显示标签 （a系列名称 b名称 c数值 d百分比）
                         )
        # 「颜色」调整. 同一色系不同深浅，取色地址 ：https://0to255.com/254,121,74。 也可设置不同色系
        # .set_colors(["#e13c01", "#fe5317", "#fe6c39", "#fe865b", "#fe865b", "#feab8e", "#ffc4af"])
        .set_colors([color_1, color_2])
    )
    st_pyecharts(c, height="550px", )  # 内置的只有light和dark，其它的需要设置或安装


def bar_phonetype(x, y, title="手机型号"):
    """条形图"""
    # x = ls_phonetype
    # y = [round(x / 100000000, 2) for x in ls_consume_phonetype]

    c = (
        Bar()
        .add_xaxis(x)
        .add_yaxis(
            "sales",
            y,
            category_gap="60%",
            color=color_1,
            bar_width=18,  # 条宽度
        )
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="right", formatter="{c}亿"))
        # 全局设置
        .set_global_opts(title_opts=opts.TitleOpts(title=title, pos_left="20%"),  # 标题，偏移与grid偏移相同
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
                                                  # boundary_gap=True,  # 中间点于「轴还是中间」,True在网格中间
                                                  is_show=False,  # x轴的轴身是否显示
                                                  # min_=0,  # 0  # x轴最小值，只在数值时起效
                                                  # max_=float(max(y) * 1.35),  # 条形图，x轴的最大值
                                                  # max_=10, # x轴最大值
                                                  # name="月份",  # y轴轴标题
                                                  # offset=-60,  # 标签与轴的距离
                                                  ),
                         yaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_show=True, ),  # 是否显示「轴线条」
                                                  splitline_opts=opts.SplitLineOpts(is_show=False),  # 去y轴网格线
                                                  # type_="log",  # 设置为「对数轴」
                                                  # is_show=True,  # y轴的轴身是否显示
                                                  # min_=0,  # y轴最小值，起始点非0
                                                  # max_=int(max(ls_consume_brand) * 1.2),  # ,200, # y轴最大值
                                                  name="金额",  # y轴轴标题
                                                  # offset=-30,  # 标签与轴的距离
                                                  position="left",  # 标签位置，左右

                                                  ),
                         tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross",
                                                       formatter="{b} {c}亿"),  # 鼠标移动时显示两轴标签
                         )
    )
    # 创建网格布局，偏移左边距
    grid = Grid()
    grid.add(c, grid_opts=opts.GridOpts(pos_left="30%", pos_right="20%"))
    # 创建网格布局
    st_pyecharts(grid, height="550px", )


def bar_area_sale(x, y, title="地区销售"):
    # x = ls_area
    # y = [round(x / 100000000, 2) for x in ls_consume_area]
    c = (
        Bar()
        .add_xaxis(x, )
        .add_yaxis("sales", y, color=color_1, )
        # .add_yaxis("商家B", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title=title, ),

                         xaxis_opts=opts.AxisOpts(is_show=True,
                                                  # is_inverse=True, # 上下翻转
                                                  boundary_gap=True,  # ? 未知
                                                  position="start",  # ? 未知
                                                  # offset=-30,  # 轴数值偏移
                                                  # min_=10000,  # 轴最小值
                                                  axislabel_opts=opts.LabelOpts(is_show=True,  # 显示标签
                                                                                rotate=45,  # 签旋转 45 度
                                                                                margin=10,  # 标签与轴线的距离为 10
                                                                                # interval="auto",  # 自动调整标签间隔
                                                                                # position="end",  # 标签显示在轴线的末端
                                                                                )
                                                  ),
                         yaxis_opts=opts.AxisOpts(is_show=True,
                                                  # is_inverse=True, # 上下翻转
                                                  boundary_gap=True,  # ? 未知
                                                  position="end",  # ? 未知
                                                  # offset=-30,  # 轴数值偏移
                                                  # min_=10000,  # 轴最小值
                                                  axislabel_opts=opts.LabelOpts(formatter="{value}亿"),  # 标签格式
                                                  ),

                         )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False, formatter="{c}亿", ),
                         markline_opts=opts.MarkLineOpts(
                             data=[opts.MarkLineItem(type_="average", name="平均值"),
                                   # opts.MarkLineItem(type_="min", name="最小值"),
                                   # opts.MarkLineItem(type_="max", name="最大值"),
                                   ]),
                         markpoint_opts=opts.MarkPointOpts(
                             data=[opts.MarkPointItem(type_="max", name="最大值", ),
                                   opts.MarkPointItem(type_="min", name="最小值"),
                                   # opts.MarkPointItem(type_="average", name="平均值"),
                                   ]),
                         tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b} {c}亿", ),  # 互动提示
                         )
    )
    st_pyecharts(c, height="350px", )


# === 四、连接pyecharts  ===
# === BI布局  ===
# 数据源展开；
# V1
with st.expander(label="（筛选后）可点击展开数据", expanded=False):
    st.dataframe(df_sizer, use_container_width=True, )
# V2 fixme ，展开器需要不受筛选器的变化旷，只收本身的状态点击改变。




try:
    with st.container():
        col1, col2 = st.columns([3, 2])
        # 此处放往入「平台筛选器」
        with col1:
            with st.container():  # border=True,
                line_month(x=ls_month, y=ls_consume_month, title='月趋势')
                bar_area_sale(x=ls_area, y=ls_consume_area, title='地区趋势')

        with col2:
            with st.container():  # border=True,
                bar_brand(ls_brand, ls_consume_brand, title='品牌排名')

    with st.container():
        col1, col2 = st.columns([2, 3])

        with col1:
            pie_sex(ls_gender, ls_consume_gender, title="性别占比")

        with col2:
            bar_phonetype(ls_phonetype, ls_consume_phonetype, title="手机型号")
except:
    st.write('绘图出错了。')
# 色系 √
# 轴标签 √
# 轴边距 √
# 关联筛选器 √
# 高度集成。
#
