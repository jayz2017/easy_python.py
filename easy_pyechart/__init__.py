from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from typing import Any, Optional, Union
from easy_pyechart import constants
from pyecharts.options.series_options import Numeric
from pyecharts.charts import Page
import random
from pyecharts.options import ComponentTitleOpts
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot
import os,gc
from plottable import Table,ColumnDefinition
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from plottable.formatters import decimal_to_percent
from plottable.plots import bar, percentile_bars, percentile_stars, progress_donut
from plottable.cmap import normed_cmap
import matplotlib
from pyecharts.globals import CurrentConfig
import math
import tempfile
import filelock
from pyecharts.globals import ThemeType

CurrentConfig.ONLINE_HOST = "http://127.0.0.1:8000//"
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
default_color_list=["#FFC125","#FF4040","#FF00FF","#C0FF3E","#9A32CD","#B03060","#48D1CC","#00EE00","#0000FF","#00F5FF","#228B22"]
matplotlib.use('Agg')  # 设置Agg为非交互式后端
class baseParams():
    def __init__(
        self,
        title: Optional[str] = None,
        subTitle: Optional[str] = None,
        themeType=constants.defualt_theme,
        backgroundImageUrl: Optional[str] = None,
    ):
        self.opts: dict = {
            "title": title,
            "subTitle": subTitle,
            "themeType": themeType,
            "backgroundImageUrl": backgroundImageUrl,
        }


'''位置上的定位定义类'''


class basePosition():
    def __init__(
        self,
        pos_left: Union[Numeric, str, None] = None,
        pos_top: Union[Numeric, str, None] = None,
        pos_right: Union[Numeric, str, None] = None,
        pos_bottom: Union[Numeric, str, None] = None
    ):
        self.opts: list = [
            pos_left,
            pos_right,
            pos_top,
            pos_bottom
        ]


'''
初始化图列的配置，
设置背景图片，或者是使用主题样式
'''


def _init_lengend(self):
    chart = self.opts['lengend']

    try:
        if self.opts['background_color_js'] != None:
            c = (
                chart(init_opts=opts.InitOpts(
                    bg_color=JsCode(self.opts['background_color_js']))
                )
            )
            return c
    except:
        # 这里的设置为异常什么都不干的原因是background_color_js是后来的属性，在没有做公共配置的其他图例中可能报错，为了不影响其他代码的执行
        ''

    backgroundImageUrl = self.opts['backgroundImageUrl']
    _initOpts = None
    if backgroundImageUrl != None and backgroundImageUrl.lstrip() != '':
        _initOpts = opts.InitOpts(
            bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"})
    else:
        _initOpts = opts.InitOpts(theme=ThemeType.DARK
                                  #self.opts['themeType']
                                  #,bg_color='#ffffff'
                                  )
    c = (
        chart(init_opts=_initOpts)
    )
    # 添加背景图片
    if backgroundImageUrl != None and backgroundImageUrl.lstrip() != '':
        _img = _setBackGroudImage_jsCode(backgroundImageUrl)
        c.add_js_funcs(
            _img
        )
    return c


def _init_grid_lengend(self):
    chart = self.opts['lengend']
    c = (
        chart(init_opts=opts.InitOpts(
            theme=self.opts['themeType'], width="1200px", height="800px")
            ,bg_color="#ffffff")
    )
    return c


'''柱状图的核心配置'''


def _get_base_example(self):
    title = self.opts['title']
    subtitle = self.opts['subTitle']
    if subtitle == None:
        subtitle = ''
    lableList = self.opts['lableList']
    valueList = self.opts['valueList']
    legendsOptsValue = self.opts['legendsOpts']
    isShowPercentage = self.opts['isShowPercentage']
    isStack = self.opts['isStack']
    backgroundImageUrl = self.opts['backgroundImageUrl']
    _category_gap = self.opts['category_gap']

    if lableList == None or type(lableList) != list or len(lableList) < 1:
        return None
    if valueList == None or type(valueList) != list or len(valueList) < 1:
        return None
    if legendsOptsValue == None or type(legendsOptsValue) != list or len(legendsOptsValue) < 1:
        return None

    c = _init_lengend(self)
    c.add_xaxis(lableList)
    for i in range(len(valueList)):
        # 是否堆叠
        if isStack == True:
            c.add_yaxis(legendsOptsValue[i], valueList[i],
                        stack="stack1", category_gap=_category_gap)
        else:
            c.add_yaxis(legendsOptsValue[i], valueList[i],
                        category_gap=_category_gap)

    if isShowPercentage != None and isShowPercentage == True:
        c.set_series_opts(
            label_opts=opts.LabelOpts(
                position="right",
                formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                ),
            )
        )
    xaxis_opts_param = None
    _max_lable_ = max(lableList)
    if (type(_max_lable_) == str and len(_max_lable_) >= 5) or (type(_max_lable_) == int and _max_lable_ >= 1000):
        xaxis_opts_param = opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=-15))
    datazoom_opts_par = None
    # 如果横坐标轴上的数据最多超过30个值，那么就开启压缩
    if len(lableList) > 30:
        datazoom_opts_par = opts.DataZoomOpts()
    try:
        c.set_global_opts(
            xaxis_opts=xaxis_opts_param,
            title_opts=opts.TitleOpts(title=title),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="shadow"),
            datazoom_opts=datazoom_opts_par
        )
    except:
        c.set_global_opts(
            xaxis_opts=xaxis_opts_param,
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="shadow"),
            datazoom_opts=datazoom_opts_par
        )
    return c


'''3D型柱状图配置'''


def _3D_base_config(self):
    chart = self.opts['lengend']
    _ydata = self.opts['ydata']
    x1_list = self.opts['x1_list']
    x2_list = self.opts['x2_list']
    chart.add(
        series_name="",
        data=_ydata,
        xaxis3d_opts=opts.Axis3DOpts(type_="category", data=x1_list),
        yaxis3d_opts=opts.Axis3DOpts(type_="category", data=x2_list),
        zaxis3d_opts=opts.Axis3DOpts(type_="value"),
    )

    chart.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            max_=20,
            range_color=[
                "#313695",
                "#4575b4",
                "#74add1",
                "#abd9e9",
                "#e0f3f8",
                "#ffffbf",
                "#fee090",
                "#fdae61",
                "#f46d43",
                "#d73027",
                "#a50026",
            ],
        )
    )
    return chart


'''饼状图的基本配置项'''


def pie_base_config(self):
    source_list = self.opts['sourceList']
    # 单行图列所布局分布
    layOutCenter = self.opts['layOutCenter']
    title = self.opts['title']
    subtitle = self.opts['subTitle']
    radius = self.opts['radius']

    c = _init_lengend(self)
    c.add_dataset(
        source=source_list
    )
    _lableList = source_list[0]
    _valueList = source_list[1:]
    for i in range(len(_valueList)):
        c.add(
            series_name=_valueList[i][0],
            data_pair=[],
            radius=radius,
            center=layOutCenter[i],
            encode={"itemName": _lableList[0], "value": _lableList[i+1]},
        )
    c.set_global_opts(
        title_opts=opts.TitleOpts(title=title, subtitle=subtitle),
        legend_opts=opts.LegendOpts(pos_left="30%", pos_top="2%"),
    )
    return c


'''涟漪图基本配置'''


def scatter_base_config(self):
    xList = self.opts['xList']
    yList = self.opts['yList']
    title = self.opts['title']
    subtitle = self.opts['subTitle']
    _symbolType = self.opts['symbolType']
    c = _init_lengend(self)
    c.add_xaxis(xList)
    for i in range(len(yList)):
        c.add_yaxis("", yList[i], symbol=_symbolType )
    c.set_global_opts(
        title_opts=opts.TitleOpts(title=title, subtitle=subtitle),
        xaxis_opts=opts.AxisOpts(
            splitline_opts=opts.SplitLineOpts(is_show=True)),
        yaxis_opts=opts.AxisOpts(
            splitline_opts=opts.SplitLineOpts(is_show=True)),
    )
    return c


'''漏斗图基本配置项'''


def _funnel_base_config(self):
    xList = self.opts['xList']
    yList = self.opts['yList']
    title = self.opts['title']
    subtitle = self.opts['subTitle']
    data = [[xList[i], yList[i]] for i in range(len(xList))]
    c = _init_lengend(self)
    c.add(
        series_name="",
        data_pair=data,
        gap=2,
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b} : {c}%"),
        label_opts=opts.LabelOpts(is_show=True, position="inside"),
        itemstyle_opts=opts.ItemStyleOpts(border_color="#fff", border_width=1),
    )
    c.set_global_opts(title_opts=opts.TitleOpts(
        title=title, subtitle=subtitle),
        )
    return c


'''仪表盘的基本配置项'''


def _gauge_base_config(self):
    c = _init_lengend(self)
    seriesName = self.opts['seriesName']
    dataList = self.opts['dataList']
    _axisline_opts = None
    if self.opts['color'] != None:
        _axisline_opts = opts.AxisLineOpts(
            linestyle_opts=opts.LineStyleOpts(
                color=self.opts['color'], width=30
            )
        )
    c.add(series_name=seriesName, data_pair=dataList,
          axisline_opts=_axisline_opts)
    c.set_global_opts(
        title_opts=opts.TitleOpts(
            title=self.opts['title'], subtitle=self.opts['subtitle']),
        legend_opts=opts.LegendOpts(is_show=False),
        tooltip_opts=opts.TooltipOpts(
            is_show=True, formatter="{a} <br/>{b} : {c}%"),
    )
    return c


'''关系图的基本配置项,简单的圆弧型设置的关系图'''


def _graph_base_config(self):
    _nodes = self.opts['nodes']
    _links = self.opts['links']
    _categories = self.opts['categories']
    c = _init_lengend(self)
 
    c.add(
        "",
        nodes=_nodes,
        links=_links,
        categories=_categories,
        layout="circular",
        is_rotate_label=True,
        linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
        label_opts=opts.LabelOpts(position="right"),
    )
    c.set_global_opts(
        title_opts=opts.TitleOpts(
            title=self.opts['title'], subtitle=self.opts['subTitle']),
        legend_opts=opts.LegendOpts(
            orient="vertical", pos_left="2%", pos_top="20%"),
    )
    return c


'''设置基本折线图的配置'''


def line_base_config(self):
    c = _init_lengend(self)
    _xaxis = None
    if  '_xaxis' in self.opts.keys() and self.opts['_xaxis'] != None:
        _xaxis = self.opts['_xaxis']
    try:
        c.add_xaxis(self.opts['xList'], xaxis=_xaxis)
    except:
        c.add_xaxis(self.opts['xList'])
    # 判断是否是圆润
    try:
        if self.opts['_is_smooth'] == True:
            _is_smooth = self.opts['_is_smooth']
    except:
        _is_smooth = None
    symbol = None
    symbol_size = None
    itemstyle_opts = None
    # 设置折线图上折点的样式
    if self.opts['symbolStype'] != None:
        symbol = self.opts['symbolStype'],
        symbol_size = 20,
        itemstyle_opts = opts.ItemStyleOpts(
            border_width=3
        )

    # 设置y轴的值
    for i in self.opts['yList']:
        _setMarkPoint = None
        _setMarkLine = None
        try:
            if i['setMarkPoint'] != None and len(i['setMarkPoint']) > 0:
                _setMarkPoint = opts.MarkPointOpts(
                    data=i['setMarkPoint']
                )
            if i['setMarkLine'] != None and len(i['setMarkLine']) > 0:
                _setMarkLine = opts.MarkLineOpts(
                    data=i['setMarkLine']
                )
        except :
            _setMarkPoint = None
            _setMarkLine = None

        if symbol != None:
            c.add_yaxis(
                series_name=i['name'],
                y_axis=i['value'],
                is_smooth=_is_smooth,
                markpoint_opts=_setMarkPoint,
                markline_opts=_setMarkLine,
                linestyle_opts=opts.LineStyleOpts(
                    width=self.opts['lineStyleWidth']),
                symbol=symbol,
                symbol_size=symbol_size,
                itemstyle_opts=itemstyle_opts
            )
        else:
            c.add_yaxis(
                series_name=i['name'],
                y_axis=i['value'],
                is_smooth=_is_smooth,
                markpoint_opts=_setMarkPoint,
                markline_opts=_setMarkLine,
                linestyle_opts=opts.LineStyleOpts(
                    width=self.opts['lineStyleWidth'])
            )
        # 如果横坐标的标签值比较长的话，就旋转一下
    xaxis_opts_param = None
    _max_lable_ = max(self.opts['xList'])
    if (type(_max_lable_) == str and len(_max_lable_) >= 5) or (type(_max_lable_) == int and _max_lable_ >= 1000):
        xaxis_opts_param = opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=-15),
            type_="category", boundary_gap=False
        )
    else:
        xaxis_opts_param = opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            type_="category",  is_scale=False, boundary_gap=False
        )
    c.set_global_opts(
        title_opts=opts.TitleOpts(
            title=self.opts['title'], subtitle=self.opts['subTitle']),
        xaxis_opts=xaxis_opts_param,
    )

    # 设置阴影
    _areastyle_opts = None
    if self.opts['areastyleOpt'] == True:
        _areastyle_opts = opts.AreaStyleOpts(opacity=0.5)
    c.set_series_opts(
        areastyle_opts=_areastyle_opts,
        label_opts=opts.LabelOpts(is_show=True),
    )
    return c

# 渐变色的折线图配置


def gradientLine_base_config(self):
    background_color_js = (
        "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
        "[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}], false)"
    )
    self.opts['background_color_js'] = background_color_js
    c = _init_lengend(self)
    area_color_js = (
        "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
        "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
    )
    c.add_xaxis(xaxis_data=self.opts['xList'])

    for i in self.opts['yList']:
        c.add_yaxis(
            series_name=i['name'],
            y_axis=i['value'],
            is_smooth=True,
            is_symbol_show=True,
            symbol="circle",
            symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(color="#fff"),
            label_opts=opts.LabelOpts(
                is_show=True, position="top", color="#ffffff"),
            # itemstyle_opts=opts.ItemStyleOpts(
            #     color="red", border_color="#fff", border_width=3
            # ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            areastyle_opts=opts.AreaStyleOpts(
                color=JsCode(area_color_js), opacity=1),
        )

    c.set_global_opts(
        title_opts=opts.TitleOpts(
            title=self.opts['title'],
            subtitle=self.opts['subTitle'],
            pos_bottom="5%",
            pos_left="center",
            title_textstyle_opts=opts.TextStyleOpts(
                color="#fff", font_size=16),
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            boundary_gap=False,
            axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
            axisline_opts=opts.AxisLineOpts(is_show=False),
            axistick_opts=opts.AxisTickOpts(
                is_show=True,
                length=25,
                linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
            ),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
            ),
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            position="right",
            axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
            ),
            axistick_opts=opts.AxisTickOpts(
                is_show=True,
                length=15,
                linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
            ),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
            ),
        ),
    )
    return c


# 水球图
def liquid_base_config(self):
    c = _init_lengend(self)
    label_opts = None
    if self.opts['labelOpts'] == True:
        label_opts = opts.LabelOpts(
            font_size=50,
            formatter=JsCode(
                """function (param) {
                    return (Math.floor(param.value * 10000) / 100) + '%';
                }"""
            ),
            position="inside",
        )
    c.add("Liquid", self.opts['yList']
          #, label_opts=label_opts
          )
    # c.set_global_opts(title_opts=opts.TitleOpts(
    #     title=self.opts['title'], subtitle=self.opts['subTitle']),
    #     )
    return c


# 平行坐标系图
def parallel_base_config(self):
    c = _init_lengend(self)
    schemaList = []
    _lableList = self.opts['lableList']
    for i in range(len(_lableList)):
        if self.opts['isLableStardFlag'] == True:
            if i == 0:
                schemaList.append(opts.ParallelAxisOpts(
                    dim=i,
                    name=_lableList[i],
                    type_=self.opts['schemaType'],
                    data=self.opts['ydata']
                )
                )
            else:
                schemaList.append(opts.ParallelAxisOpts(dim=i,
                                                        name=_lableList[i]
                                                        ))
        else:
            if i+1 == len(_lableList):
                schemaList.append(opts.ParallelAxisOpts(
                    dim=i,
                    name=_lableList[i],
                    type_=self.opts['schemaType'],
                    data=self.opts['ydata']
                )
                )
            else:
                schemaList.append(opts.ParallelAxisOpts(dim=i,
                                                        name=_lableList[i]
                                                        ))

    c.add_schema(schemaList)
    for i in self.opts['valueList']:
        c.add(i['name'], i['value'], is_smooth=self.opts['isSmooth'],
              linestyle_opts=opts.LineStyleOpts(width=self.opts['lineStyleWidth']))

    c.set_global_opts(title_opts=opts.TitleOpts(
        title=self.opts['title'], subtitle=self.opts['subTitle']),
        )
    return c

'''饼状图基本配置'''
def double_pie_base_config(self):
    c = _init_lengend(self)
    #判断是否有富文本的标签展示
    _label_opts =opts.LabelOpts(is_show=False, position="center")
    for i in self.opts['dataList']:
        if i['isRichLabel'] == True:
            _label_opts =  opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                #is_show=True,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            )
        c.add(
            series_name = i['name'],
            data_pair= i['value'],
            rosetype= i ['type'],
            radius=i ['radius'],
            center=i ['centerLayOut'],
            label_opts=_label_opts,
        )
    c.set_global_opts(
        title_opts=opts.TitleOpts(
            title=self.opts['title'],
            pos_left="center",
            pos_top="20",
            title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
        ),
        #legend_opts=opts.LegendOpts(is_show=False),
        legend_opts=opts.LegendOpts(orient="scroll", pos_top="15%", pos_left="2%" )
    )
    if self.opts['dataList'][0]['isRichLabel']==False:
        c.set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{b}: {c}"
            ),
            label_opts=opts.LabelOpts(color="red"),
        )
    return c

#雷达图的基本配置项
def radar_base_config(self):
    c = _init_lengend(self)
    _schema=[]
    for i in self.opts['lableList']:
        try:
            _schema.append(
                opts.RadarIndicatorItem(name=i["name"], max_=i["max"])
            )
        except:
            _schema.append(
                opts.RadarIndicatorItem(name=i["name"], max_=i["value"])
            )   
    _color =random.sample(default_color_list, len(self.opts['valueList']))
    c.add_schema(   schema = _schema,
                    splitarea_opt=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)  ),
                    textstyle_opts=opts.TextStyleOpts(color=_color[0]),
                )
    
    for i in range(len(self.opts['valueList'])):
        _v = self.opts['valueList'][i]
        c.add(
             series_name= _v["name"],
            data=_v["value"],
            linestyle_opts=opts.LineStyleOpts(color=_color[i]),
        )

    c.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    c.set_global_opts(
        title_opts=opts.TitleOpts(title=self.opts['title'],subtitle=self.opts['subTitle']), legend_opts=opts.LegendOpts(pos_left='legft',pos_top='15%',orient="vertical")
    )
    return c

#带有阴影区域设置的雷达图的基本配置项，而且图例的样式时圆形，而不是六角型
def round_radar_base_config(self,max,min):
    c = _init_lengend(self)
    _v = abs(max)+abs(min)
    interval = round(_v/4)
    _color =['#5470c6','#91cc75','#fac858','#ee6666','#73c0de','#457385',"#4587E7",'#74a35e','#def0d6','#bbc6e8','#98a9dd']
    # 随机选择一个颜色
    random_color = random.choice(_color)
    c.set_colors(['#000000'])
    c.add_schema(
        schema=self.opts['lableList'],
        shape="circle",
        center=["50%", "50%"],
        radius="80%",
        angleaxis_opts=opts.AngleAxisOpts(
            min_=0,
            max_=360,
            is_clockwise=False,
            interval=5,
            axistick_opts=opts.AxisTickOpts(is_show=False),
            axislabel_opts=opts.LabelOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
        ),
        radiusaxis_opts=opts.RadiusAxisOpts(
            min_=min,
            max_=max,
            interval=interval,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1,
                                                                #color=random_color
                                                                #'rgba(255, 255, 255, 0.5)'
                )
            ),
        ),
        polar_opts=opts.PolarOpts(),
        splitarea_opt=opts.SplitAreaOpts(is_show=False),
        splitline_opt=opts.SplitLineOpts(is_show=False),
    )
    c.add(
        series_name=self.opts['valueList'][0]['name'],
        data=self.opts['valueList'],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.8,color=random_color
                #                           JsCode(
                #     """ new echarts.graphic.RadialGradient(0.5, 0.5, 1, [
                #             {
                #                 color: '#B8D3E4',
                #                 offset: 0
                #             },
                #             {
                #                 color: '#72ACD1',
                #                 offset: 1
                #             }
                #         ])
                #         """
                # )
                ),
        linestyle_opts=opts.LineStyleOpts(width=1),
    )
    c.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    c.set_global_opts(
        title_opts=opts.TitleOpts(title=self.opts['title'],subtitle=self.opts['subTitle'],pos_left='20%',pos_top='10%'), legend_opts=opts.LegendOpts(pos_left='legft',pos_top='15%',orient="vertical")
    )
    return c


#定义桑基图的基本配置项
def sankey_base_config(self):
    c=_init_lengend(self)
    c.add(
        self.opts['seriesName'],
        self.opts['lableList'],
        self.opts['valueList'],
        linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"),
        label_opts=opts.LabelOpts(position="right"),
        itemstyle_opts=opts.ItemStyleOpts(border_width=1, border_color="#aaa"),
        tooltip_opts=opts.TooltipOpts(trigger_on="mousemove"),

    )
    c.set_global_opts(title_opts=opts.TitleOpts(title=self.opts['title'],subtitle=self.opts['subTitle']), legend_opts=opts.LegendOpts(pos_left='right',pos_top='10%',orient="vertical"))
    return c

#定义table表格的基本配置
def table_base_config(self):
    table =self.opts['lengend']
    c= table()
    c.add(self.opts['headerList'], self.opts['rowList'])
    c.set_global_opts(
        title_opts=ComponentTitleOpts(title=self.opts['title'], subtitle=self.opts['subTitle'])
    )
    return c

#定义树类型的数据表格基本配置
def treeMap_base_config(self):
    table=self.opts['lengend']
    c= table()
    c.add(
        series_name="option",
        data=self.opts['dataList'],
        visual_min=300,
        leaf_depth=1,
        # 标签居中为 position = "inside"
        label_opts=opts.LabelOpts(position="inside"),
    )
    c.set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False),
        title_opts=opts.TitleOpts(
            title=self.opts['title'],subtitle=self.opts['subTitle'], pos_left="leafDepth"
        ),
    )
    return c


'''定义水印 '''
def set_water_marking(waterText):
    return [
        opts.GraphicGroup(
            graphic_item=opts.GraphicItem(
                rotation=JsCode("Math.PI / 4"),
                bounding="raw",
                right=110,
                bottom=110,
                z=100,
            ),
            children=[
                opts.GraphicRect(
                    graphic_item=opts.GraphicItem(
                        left="center", top="center", z=100
                    ),
                    graphic_shape_opts=opts.GraphicShapeOpts(
                        width=400, height=50),
                    graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                        fill="rgba(0,0,0,0.3)"
                    ),
                ),
                opts.GraphicText(
                    graphic_item=opts.GraphicItem(
                        left="center", top="center", z=100
                    ),
                    graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                        text=waterText,
                        font="bold 26px Microsoft YaHei",
                        graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                            fill="#fff"
                        ),
                    ),
                ),
            ],
        )
    ]


'''设置引入小图片'''


def _set_logo_(imageUrl):
    return [
        opts.GraphicImage(
            graphic_item=opts.GraphicItem(
                id_="logo", right=20, top=20, z=-10, bounding="raw", origin=[75, 75]
            ),
            graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
                image=imageUrl,
                width=150,
                height=150,
                opacity=0.4,
            ),
        )
    ]


'''这只logo 旋转的功能，为何返回的是字符串，原因是可以与设置背景图片的那段js代码向 公共使用'''


def _set_logo_ratate():
    return """
        var rotation = 0;
        setInterval(function () {
            chart_1234.setOption({
                graphic: {
                    id: 'logo',
                    rotation: (rotation += Math.PI / 360) % (Math.PI * 2)
                }
            });
        }, 30);
    """

# 设置背景图片的js操作代码


def _setBackGroudImage_jsCode(imageUrl):
    _img = """
            var img = new Image(); img.src = '{backgroundImageUrl}';
            """
    _img = _img.format(
        backgroundImageUrl=imageUrl).replace('\\', '\\\\')
    return _img


'''定义多个图表组合的页面配置方式，grid 平行组件'''


def _grid_base_config(self):
    c = _init_grid_lengend(self)
    _charts = self.opts['charts']
    for i in _charts:
        # 左右上下4个值
        _pos = i['position']
        if len(_pos) != 4:
            return
        c.add(i['chart'], grid_opts=opts.GridOpts(pos_left=_pos[0],
              pos_right=_pos[1], pos_top=_pos[2], pos_bottom=_pos[3]), is_control_axis_index=True)
    return c


'''页面组件的设置'''


def _page_layout_base_config(self):
    page = Page(layout=Page.DraggablePageLayout)
    for i in self.opts['charts']:
        page.add(i)
    return i


#保存为图片
def save_static_image(tagertLengend,tagertPath):
    temp_dir=r"C:\haochenkeji\sameTimeJpg"
    # 创建临时文件，指定临时文件的存放目录
    with tempfile.NamedTemporaryFile(delete=False, dir=temp_dir, suffix=".html") as tmp_file:
        temp_path = tmp_file.name
        # 渲染图表到临时文件
        tagertLengend.render(temp_path)
        # 使用文件锁确保删除操作的安全性
        try:
            # 生成静态图像
            make_snapshot(snapshot, temp_path, tagertPath, is_remove_html=False)
        except Exception as e:
            print(f"保存图片失败: {e}")
       # finally:
            # 删除临时文件
            #os.remove(temp_path)


    # #try:
    #     make_snapshot(snapshot, tagertLengend.render(), tagertPath,is_remove_html=True)
    # #int("保存图片失败")    
    #     os.remove(tagertLengend.render())

def table_base_config(self,lineSplit):
    page_wight = self.opts["page_wight"]
    page_hight = self.opts["page_hight"]
    columns = self.opts["columns"]
    _data = self.opts["_data"]
    head_colors = self.opts["head_colors"]
    head_width = self.opts["head_width"]
    the_row_color = self.opts["the_row_color"]
    line_comp_ratio = self.opts["line_comp_ratio"]

    the_row_font_size = self.opts["the_row_font_size"]
    the_column_font_size = self.opts["the_column_font_size"]
    the_column_font_color = self.opts["the_column_font_color"]

    ncols, nrows = len(columns), len(_data)
    column_definitions_list=[]
    for i in range(len(columns)):
        _dd_width = head_width.get(i,None)
        if i==0:
            column_definitions_list.append(ColumnDefinition(
                name=columns[i],
                title="",
                textprops={"ha": "left"},
                width=_dd_width if _dd_width is not None else 0.35
                #plot_fn=circled_image,
            ))
            #设置列边框的分割线
        elif lineSplit!=None and i in lineSplit :
            column_definitions_list.append(ColumnDefinition(
                name=columns[i],
                title="",
                textprops={"ha": "center"},
                width=_dd_width if _dd_width is not None else 0.2,
                border="l"
            ))
        else:
            column_definitions_list.append(ColumnDefinition(
                name=columns[i],
                title="",
                textprops={"ha": "center"},
                width=_dd_width if _dd_width is not None else 0.2,
                #plot_fn=circled_image,
            ))

    d = pd.DataFrame(_data
                , columns=columns
                 ).round(2)
    
    fig, ax = plt.subplots(figsize=(page_wight/100, page_hight/100))
       # 添加水印
    if  self.opts["water_mark"]!=None:
        ax.text(
            0.5, 0.5, 'Sample Watermark',  # 文本内容
            transform=ax.transAxes,  # 使用轴坐标系
            fontsize=40,  # 字体大小
            color='gray',  # 字体颜色
            alpha=0.2,  # 透明度
            ha='center',  # 水平对齐方式
            va='center',  # 垂直对齐方式
            rotation=30  # 文本旋转角度
        )
    tab = Table(d, 
                row_dividers=False, 
               # odd_row_color="#f0f0f0", 
                #even_row_color="#e0f6ff",
                index_col= columns[0]
                ,column_definitions=column_definitions_list,
                # row_divider_kw={"linewidth": 1, 
                #                 #"linestyle": (3, (1, 5))
                #                 },
                )    
    #设置行颜色
    for i in range(nrows):
        if str(i) in the_row_color.keys()  :
            tab.rows[i].set_facecolor(the_row_color.get(str(i)))     

    for i in  head_colors.keys():      
        #设置表格列颜色
        col =tab.columns.get(i,None)
        if col !=None : 
            tab.columns[i].set_facecolor(head_colors[i])

    for i in  the_row_font_size.keys():      
        #设置表格列字体大小
        col =tab.rows.get(i,None)
        if col !=None : 
            tab.rows[i].set_fontsize(the_row_font_size[i])

    for i in  the_column_font_size.keys():      
        #设置表格列字体大小
        col =tab.rows.get(i,None)
        if col !=None : 
            tab.rows[i].set_fontsize(the_column_font_size[i])

    for i in  the_column_font_color.keys():      
        #设置表格列字体大小
        col =tab.rows.get(i,None)
        if col !=None : 
            tab.rows[i].set_fontcolor(the_column_font_color[i])
    fig.subplots_adjust(top=0.95)  
    _image_save_link=self.opts["_image_save_link"]
    try:
        fig.savefig(_image_save_link, 
                            bbox_inches='tight', 
                            pad_inches=0,dpi=600)
    except Exception as e:
        print("生成表格图时出现问题:",e)
        plt.close()
    finally:        
        # 关闭图形对象
        plt.close()
        # 删除对图形对象的引用
        del fig
        del ax
        # 手动触发垃圾回收
        gc.collect()   
    return  None
          
def double_head_config(self,groupHeader,lineSplit):
    page_wight = self.opts["page_wight"]
    page_hight = self.opts["page_hight"]
    columns = self.opts["columns"]
    _data = self.opts["_data"]
    head_colors = self.opts["head_colors"]
    head_width = self.opts["head_width"]
    the_row_color = self.opts["the_row_color"]
    line_comp_ratio = self.opts["line_comp_ratio"]
    _image_save_link=self.opts["_image_save_link"]
    the_row_font_size = self.opts["the_row_font_size"]
    the_column_font_size = self.opts["the_column_font_size"]
    the_column_font_color = self.opts["the_column_font_color"]
    the_auto_line_color= self.opts["the_auto_line_color"]
    #指定圆圈形状的列
    the_donut_col= self.opts["the_donut_col"]
    #指定星星图案形状的列
    the_stars_col= self.opts["the_stars_col"]
    #指定进度条图案形状的列
    the_bar_col= self.opts["the_bar_col"]
    #指定条柱样式图形的列
    the_bars_col= self.opts["the_bars_col"]

    # 设置颜色
    cmap = LinearSegmentedColormap.from_list(
        name="bugw", colors=["#0ebeff", "#1db6fa", "#2caff6", "#3ba7f1", "#4a9fec","#5997e7","#6890e3"
                             ,"#7788de","#8780d9","#8780d9","#a571d0","#b469cb","#c361c6","#d259c1","#e152bd","#f04ab8"
                             ,"#ff42b3"
                             ], N=256
    )
    d = pd.DataFrame(_data
                , columns=columns
                 ).round(2)

    ncols, nrows = len(columns), len(_data)
    column_definitions_list=[]
    for i in range(len(columns)):
        _dd_width = head_width.get(str(i),None)
        #获取列的组名称，列融合的方式
        group_name=None    
        if  groupHeader is not None :  
            for f in groupHeader.keys():
                if str(i) in f.split(','):
                    group_name= groupHeader[f]
                    break
        border_wight=None       
            #设置列边框的分割线
        if lineSplit!=None and i in lineSplit :
            border_wight="l"
        _atitle =columns[i] if columns[i]!=' ' else '1',
        _atitle_str= str(_atitle[0])
        _atitle_str_r =' ' if _atitle_str.find('InvalidIdentifier')>-1  else _atitle_str,
        _atitle_str= str(_atitle_str_r[0])
        at_index = _atitle_str.find('@')
        if at_index>-1:
            _atitle_str= _atitle_str[:at_index]
        if i==1:
            column_definitions_list.append(ColumnDefinition(
                name=columns[i],
                title=_atitle_str,
                textprops={"ha": "center"},
                width=_dd_width if _dd_width is not None else 0.35,
                group=group_name if group_name is not None else None,
                border=border_wight
            ))
        elif  columns[i] in the_auto_line_color:
            column_definitions_list.append(ColumnDefinition(
                name= columns[i],
                title=_atitle_str,
                textprops={
                    "ha": "center",
                    "bbox": {"boxstyle": "circle", "pad": 0.35},
                },
                width=_dd_width if _dd_width is not None else 0.2,
                group = group_name if group_name is not None else None,
                border=border_wight,
                cmap=normed_cmap(d[columns[i]], cmap=matplotlib.cm.PiYG_r, num_stds=2.5),
            ))
        elif columns[i] in the_donut_col:
            #图案为圆形，用弧度显然数据
            column_definitions_list.append(ColumnDefinition(
                name= columns[i],
                title=_atitle_str,
                textprops={
                    "ha": "center",
                },
                width=_dd_width if _dd_width is not None else 0.2,
                group = group_name if group_name is not None else None,
                border=border_wight,
                plot_fn=progress_donut, 
                 plot_kw={
                    "is_pct": True,
                    "formatter": "{:.0%}"
                },
            ))
        elif columns[i] in the_stars_col:
            #图案为星星，用星的数量显然数据
            column_definitions_list.append(ColumnDefinition(
                name= columns[i],
                title=_atitle_str,
                textprops={
                    "ha": "center",
                },
                width=1.5,
                group = group_name if group_name is not None else None,
                border=border_wight,
                plot_fn=percentile_stars, 
                 plot_kw={
                    "is_pct": True,
                },
            ))
        elif columns[i] in the_bar_col:
              #图案为圆形，用弧度显然数据
            column_definitions_list.append(ColumnDefinition(
                name= columns[i],
                title=_atitle_str,
                textprops={
                    "ha": "center",
                },
                width=1.25,
                group = group_name if group_name is not None else None,
                border=border_wight,
                plot_fn=bar, 
                plot_kw={
                    "cmap": cmap,
                    "plot_bg_bar": True,
                    "annotate": True,
                    "height": 0.5,
                    "lw": 0.5,
                    "formatter": decimal_to_percent,
                },
            ))
        elif  columns[i] in the_bars_col:
             #图案为竖线，用竖线的数量显然数据
            column_definitions_list.append(ColumnDefinition(
                name= columns[i],
                title=_atitle_str,
                textprops={
                    "ha": "center",
                },
                group = group_name if group_name is not None else None,
                border=border_wight,
                plot_fn=percentile_bars, 
                 plot_kw={
                    "is_pct": True,
                },
            ))
        else :
            column_definitions_list.append(ColumnDefinition(
                name= columns[i],
                title=_atitle_str,
                textprops={"ha": "center"},
                width=_dd_width if _dd_width is not None else 0.2,
                group = group_name if group_name is not None else None,
                border=border_wight,
            ))    
    fig, ax = plt.subplots(figsize=(page_wight/100, page_hight/100))
    # 添加水印
    if  self.opts["water_mark"]!=None:
        ax.text(
            0.5, 0.5, 'Sample Watermark',  # 文本内容
            transform=ax.transAxes,  # 使用轴坐标系
            fontsize=40,  # 字体大小
            color='gray',  # 字体颜色
            alpha=0.2,  # 透明度
            ha='center',  # 水平对齐方式
            va='center',  # 垂直对齐方式
            rotation=30  # 文本旋转角度
        )
    tab = Table(d, 
                textprops={"ha": "center"},
                index_col= columns[0],
                column_definitions=column_definitions_list,
                row_dividers=True,
                footer_divider=True,
                row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
                col_label_divider_kw={"linewidth": 1, "linestyle": "-"},
                )
    #设置列自动的渐变色趋势
    if len(the_auto_line_color)>0:
        tab.autoset_fontcolors(colnames=the_auto_line_color)
    #设置行颜色
    #if len(the_auto_line_color)==0:
    for i in range(nrows):
        if str(i) in the_row_color.keys():
            tab.rows[i].set_facecolor(the_row_color.get(str(i)))  
    
    for i in  head_colors.keys():      
            #设置表格列颜色
            col =tab.columns.get(i,None)
            if col !=None : 
                tab.columns[i].set_facecolor(head_colors[i])

    for i in  the_row_font_size.keys():      
        #设置表格列字体大小
        col =tab.rows.get(i,None)
        if col !=None : 
            tab.rows[i].set_fontsize(the_row_font_size[i])

    for i in  the_column_font_size.keys():      
        #设置表格列字体大小
        col =tab.rows.get(i,None)
        if col !=None : 
            tab.rows[i].set_fontsize(the_column_font_size[i])

    for i in  the_column_font_color.keys():      
        #设置表格列字体颜色
        col =tab.rows.get(i,None)
        if col !=None : 
            tab.rows[i].set_fontcolor(the_column_font_color[i])
    fig.subplots_adjust()
    try:
        fig.savefig(_image_save_link, 
                            bbox_inches='tight', 
                            pad_inches=0,dpi=600)
    except Exception as e:
        print("生成表格图时出现问题:",e)
        plt.close()
    finally:        
        # 关闭图形对象
        plt.close()
        # 删除对图形对象的引用
        del fig
        del ax
        # 手动触发垃圾回收
        gc.collect()   
    return  None


# #保存为图片
# def save_static_image(tagertLengend,tagertPath):
#     try:
#         make_snapshot(snapshot, tagertLengend.render(), tagertPath
#                       ,is_remove_html=True
#                       )
    
#         #print("截取完图片的时间："+ str(time.time()))
#         return  tagertPath
#     except Exception as e:
#         print("保存图片失败",e)    
#         os.remove(tagertLengend.render())