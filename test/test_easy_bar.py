import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from easy_pyechart import easy_Bar,set_water_marking,save_static_image

#测试柱状图中最简单的图例模式
def _test_eBar():
    _value_list_ =[]
    _value_list_.append([
            {"value": 12, "percent": 12 / (12 + 3)},
            {"value": 23, "percent": 23 / (23 + 21)},
            {"value": 33, "percent": 33 / (33 + 5)},
            {"value": 3, "percent": 3 / (3 + 52)},
            {"value": 33, "percent": 33 / (33 + 43)},
        ])
    _value_list_.append([
            {"value": 3, "percent": 3 / (12 + 3)},
            {"value": 21, "percent": 21 / (23 + 21)},
            {"value": 5, "percent": 5 / (33 + 5)},
            {"value": 52, "percent": 52 / (3 + 52)},
            {"value": 43, "percent": 43 / (33 + 43)},
        ])
    _p=easy_Bar.eBar(title='这个是图',lableList=[1, 2, 3, 4, 5],valueList=_value_list_,legendsOpts=['product1','product2']
                    # ,backgroundImageUrl=r'C:\Users\chenhao\Desktop\客户调休回复邮件报告.png'
                     )._stack_bar_percent()
    _p.render("stack_bar_percent.html")

#_test_eBar()

def _test_bar_line():
    _lableList=["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    _value_list_ =[]
    _value_list_.append([2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3])
    _value_list_.append([2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3])
    _extra_value_=[2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2]
    _p=easy_Bar.eBar(title='这个是图',lableList=_lableList,valueList=_value_list_,legendsOpts=['蒸发量','降水量'])._mixed_bar_and_line(extraYname='温度',extraYList=_extra_value_,extraLegendName='平均温度')
    _p.set_global_opts(graphic_opts=set_water_marking('牛逼2121class'))
    #_p.render("mixed_bar_and_line.html")
    save_static_image(_p,"2223211.png")
    
_test_bar_line()
