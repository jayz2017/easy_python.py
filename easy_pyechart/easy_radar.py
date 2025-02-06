import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pyecharts import options as opts
from typing import Any,Optional
from pyecharts.charts import Radar
from easy_pyechart import constants,baseParams,radar_base_config,round_radar_base_config


class eRadar():
    def __init__(
        self,
        lableList:Optional[list] = [],
        valueList:Optional[list] = [],
    ):
        self.opts: dict = {
                           "lengend":Radar,
                           "lableList":lableList,
                           "valueList":valueList,
                           }

    #基本雷达图    
    def basic_radar_chart(self,baseParams):
        self.opts.update(baseParams.opts)
        return radar_base_config(self)
    
    #单选模式
    def radar_selected_mode(self,baseParams):
        self.opts.update(baseParams.opts)
        c=radar_base_config(self)
        c.set_global_opts(
                legend_opts=opts.LegendOpts(selected_mode="single"),
                title_opts=opts.TitleOpts(title=self.opts['title'],subtitle=self.opts['subTitle'],))  
        return c 
    
    #
    def radar_air_quality(self,baseParams):
        self.opts.update(baseParams.opts)
        return radar_base_config(self)
    
    #设置带有阴影区域的雷达图
    def radar_angle_radius_axis(self,baseParams,max,min):
        self.opts.update(baseParams.opts)
        return     round_radar_base_config(self,max,min)   