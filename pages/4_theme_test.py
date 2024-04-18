###
# 结论：网上暂无可直接一键使用主题的方法，需要自定义主题。
# 其它方式：1、单数据设置 ；2、绕到html渲染。3、改用pyecharts。 4 、使用自定义主题色系。
#
#


###
from streamlit_echarts import st_pyecharts

from pyecharts import options as opts
from pyecharts.charts import Bar, Page
from pyecharts.faker import Collector, Faker
from pyecharts.globals import ThemeType

# from pyecharts import configure

# 将这行代码置于首部
# configure(global_theme='dark')


C = Collector()

from pyecharts.globals import CurrentConfig
import json

# 导入自定义主题
# with open(r"D:\Code\My_project\b_变现测试\BI看板\st看板\pages\vintage.json", "r", encoding="utf-8") as f:
#     vintage_theme = json.load(f)
#
# # 将自定义主题添加到当前配置中
# CurrentConfig.ONLINE_HOST = vintage_theme


# def theme_test():
#     c = (
#         Bar()
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts(title="Bar-test"))
#     )
#
#     # 添加自定义主题
#     # c.add_js_funcs("echarts.registerTheme('vintage', {})".format(json.dumps(vintage_theme)))
#
#     st_pyecharts(c, theme="vintage")  # 使用自定义主题


# theme_test()


def theme_default():
    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .add_yaxis("商家C", Faker.values())
        .add_yaxis("商家D", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-default"))
    )
    st_pyecharts(c, theme="default")


theme_default()


def theme_light() -> Bar:
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .add_yaxis("商家C", Faker.values())
        .add_yaxis("商家D", Faker.values())
        # .set_global_opts(title_opts=opts.TitleOpts(title="Bar-default"))
        .set_global_opts(title_opts=opts.TitleOpts(title="Theme-light"))
    )
    st_pyecharts(c, theme="light")  # 内置的


theme_light()


def theme_dark():
    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .add_yaxis("商家C", Faker.values())
        .add_yaxis("商家D", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="Theme-dark"))
    )
    st_pyecharts(c, theme="dark")  # 内置的


theme_dark()
#
# @C.funcs
# def theme_chalk() -> Bar:
#     c = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts("Theme-chalk"))
#     )
#     return c
#
#
# @C.funcs
# def theme_essos() -> Bar:
#     c = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts("Theme-essos"))
#     )
#     return c
#
#
# @C.funcs
# def theme_infographic() -> Bar:
#     c = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.INFOGRAPHIC))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts("Theme-infographic"))
#     )
#     return c
#
#
# @C.funcs
# def theme_macarons() -> Bar:
#     c = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts("Theme-macarons"))
#     )
#     return c
#
#
# @C.funcs
# def theme_purple_passion() -> Bar:
#     c = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts("Theme-purple-passion"))
#     )
#     return c
#
#
# @C.funcs
# def theme_roma() -> Bar:
#     c = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts("Theme-roma"))
#     )
#     return c
#
#
# @C.funcs
# def theme_romantic() -> Bar:
#     c = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.ROMANTIC))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts("Theme-romantic"))
#     )
#     return c
#
#
# @C.funcs
# def theme_shine() -> Bar:
#     c = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.SHINE))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts("Theme-shine"))
#     )
#     return c
#
#
# @C.funcs
# def theme_vintage() -> Bar:
#     c = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts("Theme-vintage"))
#     )
#     return c
#
#
# @C.funcs
# def theme_walden() -> Bar:
#     c = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.WALDEN))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts("Theme-walden"))
#     )
#     return c
#
#
# @C.funcs
# def theme_westeros() -> Bar:
#     c = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts("Theme-westeros"))
#     )
#     return c
#
#
#
#
# @C.funcs
# def theme_wonderland() -> Bar:
#     c = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.WONDERLAND))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .add_yaxis("商家C", Faker.values())
#         .add_yaxis("商家D", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts("Theme-wonderland"))
#     )
#     st_pyecharts(c)
#     # return c
#
# theme_wonderland()
#
#
#
