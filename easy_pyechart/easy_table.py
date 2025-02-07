import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pyecharts import options as opts
from typing import Any,Optional
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from easy_pyechart import constants,baseParams,table_base_config
import matplotlib.pyplot as plt

class eTable():
    def __init__(
        self,
        headerList:Optional[list] = [],
        rowList:Optional[list] = [],
          columnColor:Optional[list] = []
    ):
        self.opts: dict = {
                           "lengend":Table,
                           "headerList":headerList,
                           "rowList":rowList,
                           }
        
    def base_table(self,baseParams):
        self.opts.update(baseParams.opts)
        return table_base_config(self)

class eMTable():
    def __init__(
        self,
        rowList:Optional[list] = [],
        columnColor:Optional[list] = [],
        outSaveUrl:Optional[str] =None
        ):
        self.opts: dict = {
                           "lengend":Table,
                           "columnColor":columnColor,
                           "rowList":rowList,
                           'outSaveUrl':outSaveUrl
                           }
    def base_table(self):
        # 设置图像大小  
        figsize = (8, 6)  
        fig, ax = plt.subplots(figsize=figsize)
        # 隐藏坐标轴
        ax.axis("off")
        table = ax.table(cellText=self.opts['rowList'], 
                         #cellColours=self.opts['columnColor'], 
                         cellLoc='center',
                         loc="center")
      
        colors = ['lightblue', 'pink', 'lightgreen', 'yellow', 'lightcoral']
        # 设置列宽和行高  
        for (i, j), cell in table.get_celld().items():  
            cell.set_width(0.25)  
            cell.set_height(0.08)
            cell.set_facecolor('lightblue')  
                # 设置表格属性（可选） 
        table.auto_set_font_size(False)  
        table.set_fontsize(18)  
        table.scale(1, 1.5)  # 调整表格大小  
        plt.savefig(self.opts['outSaveUrl'],bbox_inches='tight', pad_inches=0)



#eMTable(rowList=[[1, 2, 3,3,4,4,4,4,4], [4, 5, 6,3,4,4,4,4,4], [7, 8, 9,3,4,4,4,4,4], [7, 8, 9,3,4,4,4,4,4], [7, 8, 9,3,4,4,4,4,4], [7, 8, 9,3,4,4,4,4,4], [7, 8, 9,3,4,4,4,4,4]],outSaveUrl='www.png').base_table()