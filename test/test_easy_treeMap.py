# import re
# import asyncio
# from aiohttp import TCPConnector, ClientSession
# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from easy_pyechart import easy_treeMap,baseParams


# async def get_json_data(url: str) -> dict:
#     async with ClientSession(connector=TCPConnector(ssl=False)) as session:
#         async with session.get(url=url) as response:
#             return await response.json()


# # 获取官方的数据
# data = asyncio.run(
#     get_json_data(
#         url="https://echarts.apache.org/examples/data/asset/data/"
#         "ec-option-doc-statistics-201604.json"
#     )
# )

# tree_map_data: dict = {"children": []}


# def convert(source, target, base_path: str):
#     for key in source:
#         if base_path != "":
#             path = base_path + "." + key
#         else:
#             path = key
#         if re.match(r"/^\$/", key):
#             pass
#         else:
#             child = {"name": path, "children": []}
#             target["children"].append(child)
#             if isinstance(source[key], dict):
#                 convert(source[key], child, path)
#             else:
#                 target["value"] = source["$count"]


# convert(source=data, target=tree_map_data, base_path="")
# easy_treeMap.eTreeMap(dataList=tree_map_data['children']).echarts_option(baseParams(title='3323223')).render("treemap_levels.html")
