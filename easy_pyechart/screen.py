import glob
from PIL import Image
from selenium import webdriver
import os
from io import BytesIO

def screen_png(file_location,save_path):
    file_location ="file://" + file_location
    file_type = save_path.split(".")[-1]
    # open in webpage
    driver = webdriver.Chrome()
        # The above line could be substituted for these 3 lines,
        # which would prevent the webpage from opening first
        ###########
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path="C:\\haochenkeji\\driver\\chromedriver.exe", chrome_options=options)
        # Your path to your chromedriver could be different than mine
        ###########

    driver.get(file_location)
    save_name = save_path.split(".")     
    driver.save_screenshot(save_name)
    driver.quit()
        # crop as required
    img = Image.open(BytesIO(save_name))
    box = (1, 1, 1000, 1000)
    area = img.crop(box)
    area.save(save_path)


#screen_png(r'D:\plg_resource\easy_pyechartpy\table_base.html',"customized_pie.png")