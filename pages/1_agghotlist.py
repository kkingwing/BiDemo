
import streamlit as st
from datetime import datetime


import pandas as pd

st.set_page_config(
    page_title='热搜榜聚合',  # 浏览器的标签标题，
    page_icon='🔥',  # 标签图标，支持emoji
    layout='wide',  # 主区域布局，默认为「居中的centered「，也可以选为「布满的wide」
    initial_sidebar_state='auto',
    menu_items={  # 右上角文字链接，键为固定字符串
        'Get Help': 'https://www.extremelycoolapp.com/help',
    }

)
# st.title('热搜榜聚合')

CON = st.connection("mydb", type="sql", autocommit=True)
# === 读取sql数据作为「预置数据」以备使用 , 下面的写法是st专用方法===
sql = 'SELECT * FROM `aggregate_hot_list`'
# df = pd.read_sql(sql=sql, con=CON)  #st不这么调用，注释掉
df = CON.query(sql)
# print(CON)
TODAY = datetime.now().strftime("%Y-%m-%d")

st.subheader(' 📰**热榜聚合** ' + TODAY)
st.divider()

# 1. 读取sql的「知乎」热榜数据
df_zhihu = df[(df['平台'] == '知乎') & (df['记录日期'] == TODAY)][:]
zh_titles = list(df_zhihu['标题'])
zh_urls = list(df_zhihu['url'])
zh_hots = list(df_zhihu['热度'])

# 2.读取sql的「微博」热榜数据
df_weibo = df[(df['平台'] == '微博') & (df['记录日期'] == TODAY)][:]
wb_titles = list(df_weibo['标题'])
wb_urls = list(df_weibo['url'])
wb_hots = list(df_weibo['热度'])

# 3.读取sql的「百度」热榜数据
df_baidu = df[(df['平台'] == '百度') & (df['记录日期'] == TODAY)][:]
baidu_titles = list(df_baidu['标题'])
baidu_urls = list(df_baidu['url'])
baidu_hots = list(df_baidu['热度'])

# 4.读取sql的「IT之家」热榜数据
df_ithome = df[(df['平台'] == 'IT之家') & (df['记录日期'] == TODAY)][:]
ithome_titles = list(df_ithome['标题'])
ithome_urls = list(df_ithome['url'])
ithome_hots = list(df_ithome['热度'])

# 5.读取sql的「总热度」，当前热度标准不一，后需要标准化
df_all = df[(df['记录日期'] == TODAY)][:20]
all_platforms = list(df_all['平台'])
all_titles = list(df_all['标题'])
all_urls = list(df_all['url'])
all_hots = list(df_all['热度'])


def to_wan_hot(hot):
    """
    将微博的数字转换为万的单位并加上文本 "万热度"

    Args:
        hot: 数字型文本

    Returns:
        str: 转换后的文本
    """
    if not hot:
        return ""
    try:
        hot_num = float(hot)
        if hot_num >= 10000:
            return f"{hot_num / 10000:.1f} 万热度"
        else:
            return f"{hot:.0f}"
    except ValueError:
        return hot


# === 以下为「页面布局」及「读取预置数据」。
# st.tabs() # 标签布局
tab_all, tab_hotlist = st.tabs(["总榜", "热搜榜"])
with tab_all:
    # === 容器 ===
    with st.container(border=True, height=520):
        st.caption('总热榜')
        for i, (title, url, hot, platform) in enumerate(zip(all_titles, all_urls, all_hots, all_platforms)):
            md_all = f"{i + 1}. |{platform}|    [{title}]({url})  :red[{to_wan_hot(hot)}]\n"
            st.write(md_all)
        st.divider()

# 布局： tab标签
with tab_hotlist:
    col1, col2, col3, col4 = st.columns([0.35, 0.35, 0.35, 0.35])  # 分组栏
    # === 分组栏 ===
    with col1:
        # === 容器 ===
        with st.container(border=True, height=520):
            st.caption('知乎')
            for i, (title, url, hot) in enumerate(zip(zh_titles, zh_urls, zh_hots)):
                md_zhihu = f"{i + 1}. [{title}]({url})  :red[{to_wan_hot(hot)}]\n"
                st.write(md_zhihu)
            st.divider()

    with col2:
        with st.container(border=True, height=520):
            st.caption('微博')
            # st.divider()
            for i, (title, url, hot) in enumerate(zip(wb_titles, wb_urls, wb_hots)):
                md_zhihu = f"{i + 1}. [{title.strip('#')}]({url})  :red[{to_wan_hot(hot)}]\n"
                st.write(md_zhihu)
            st.divider()

    with col3:
        with st.container(border=True, height=520):
            st.caption('百度')
            # st.divider()
            for i, (title, url, hot) in enumerate(zip(baidu_titles, baidu_urls, baidu_hots)):
                md_zhihu = f"{i + 1}. [{title}]({url})  :red[{to_wan_hot(hot)}]\n"
                st.write(md_zhihu)
            st.divider()

    with col4:
        with st.container(border=True, height=520):
            st.caption('IT之家')
            # st.divider()
            for i, (title, url, hot) in enumerate(zip(ithome_titles, ithome_urls, ithome_hots)):
                md_zhihu = f"{i + 1}. [{title}]({url})  :red[{to_wan_hot(hot)}]\n"
                st.write(md_zhihu)
            st.divider()
