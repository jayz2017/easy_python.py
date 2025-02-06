from pyecharts.globals import ThemeType

# 默认主题样式
defualt_theme = ThemeType.ROMANTIC
# 默认可选择的主题样式集合
defualt_theme_list = [ThemeType.LIGHT, ThemeType.DARK, ThemeType.CHALK, ThemeType.ESSOS,
                      ThemeType.INFOGRAPHIC, ThemeType.MACARONS, ThemeType.PURPLE_PASSION, ThemeType.ROMA, ThemeType.ROMANTIC, ThemeType.SHINE,
                      ThemeType.VINTAGE,
                      ThemeType.WALDEN,
                      ThemeType.WESTEROS,
                      ThemeType.WONDERLAND
                      ]

#
defualt_treeMap_sourse_dict={
    "name":"",
    "value":"",
    "children":[]
}

# def convert_treeMap_sourse(sourse):
#     #如果不是集合则跳出去
#     if type(sourse) !=list:
#         return 
#     for i in sourse:

