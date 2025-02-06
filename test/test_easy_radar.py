import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from easy_pyechart import easy_radar,baseParams
from pyecharts.commons.utils import JsCode

lable_list = [{
    "name":"销售（sales）",
    "value":6500
},{
    "name":"管理（Administration）",
    "value":16000
},{
    "name":"信息技术（Information Technology）",
    "value":30000
},{
    "name":"客服（Customer Support）",
    "value":38000
},{
    "name":"研发（Development）",
    "value":52000
},{
    "name":"市场（Marketing）",
    "value":25000
}]
value_list=[{
  "name":"预算分配（Allocated Budget）",
  "value":[[4300, 10000, 28000, 35000, 50000, 19000]]

},{
  "name":"实际开销（Actual Spending）",
  "value":[[5000, 14000, 28000, 31000, 42000, 21000]]
}]

#easy_radar.eRadar(lableList=lable_list,valueList=value_list).basic_radar_chart(baseParams=baseParams(title='测试一下')).render("basic_radar_chart.html")
#easy_radar.eRadar(lableList=lable_list,valueList=value_list).radar_selected_mode(baseParams=baseParams(title='测试一下')).render("basic_radar_chart.html")


data = [{"value": [[4, 2, 2, 3, 0, 1]], "name": "预算分配"},
        {"value": [[2, 1, 3, 4, 1, 1]], "name": "xx分配"},
        {"value": [[1, -4, 2, 3, 3, 4]], "name": "rr"},
        {"value": [[3, -3, 2, 3, 2, 1]], "name": "tt"}]
c_schema = [
    {"name": "销售", "max": 4, "min": -4},
    {"name": "管理", "max": 4, "min": -4},
    {"name": "技术", "max": 4, "min": -4},
    {"name": "客服", "max": 4, "min": -4},
    {"name": "研发", "max": 4, "min": -4},
    {"name": "市场", "max": 4, "min": -4},
]

#easy_radar.eRadar(lableList=c_schema,valueList=data).radar_air_quality(baseParams=baseParams(title='测试一下')).render("basic_radar_chart.html")


data = [{"value": ["2", "1", "0.5", "0.3", "0", "2","1","3"], "name": ""}]
# c_schema = [
#     {"name": "销售", "max": 22, "min": -4},
#     {"name": "管理", "max": 8, "min": -4},
#     {"name": "技术", "max": 8, "min": -4},
#     {"name": "客服", "max": 8, "min": -4},
#     {"name": "研发", "max": 8, "min": -4},
#     {"name": "市场", "max": 8, "min": -4},
# ]
c_schema =[
  {"name":"得分","max":6,"min":-2},
 {"name":"篮板","max":6,"min":-2},
 {"name":"助攻","max":6,"min":-2},
 {"name":"抢断盖帽","max":6,"min":-2},
 {"name":"失误","max":6,"min":-2},
 {"name":"效率","max":6,"min":-2},
 {"name":"影响力","max":6,"min":-2},
 {"name":"额外奖励","max":6,"min":-2}
]

#easy_radar.eRadar(lableList=c_schema,valueList=data).radar_angle_radius_axis(baseParams=baseParams(title='测试一下'),max=6,min=-2).render("basic_radar_chart.html")




from pyecharts import options as opts  
from pyecharts.charts import Radar  
  
# 数据  
data = [  
    {  
        "value": [4233, 3222, 2111,11152, 43111],  
        "name": "预算分配（Budget vs spending）"  
    }  
]  
  
# 配置项  
radar = (  
    Radar()  
    .add_schema(  
        schema=[  
            opts.RadarIndicatorItem(name="销售", max_=6500),  
            opts.RadarIndicatorItem(name="管理", max_=16000),  
            opts.RadarIndicatorItem(name="信息技术", max_=30000),  
            opts.RadarIndicatorItem(name="客户支持", max_=38000),  
            opts.RadarIndicatorItem(name="研发", max_=52000),  
        ],  
    )  
    .add("预算 vs 开销", data, 
           areastyle_opts=opts.AreaStyleOpts(opacity=1,color=JsCode(
                    """ new echarts.graphic.RadialGradient(0.5, 0.5, 1, [
                            {
                                color: '#B8D3E4',
                                offset: 0
                            },
                            {
                                color: '#72ACD1',
                                offset: 1
                            }
                        ])
                    """
                )
                )
       )  
    .set_series_opts(linestyle_opts=opts.LineStyleOpts(color="#47EDFC", width=1))  
    .set_global_opts(title_opts=opts.TitleOpts(title="雷达图示例"))  
)  
  
# 渲染图表  
#radar.render("basic_radar_chart1.html")