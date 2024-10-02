# ==============================
# Describe:自动监测有无着火点并定位
# D&P Author:             刘语馨
# Environment:    Python   3.11
# Create Date:       2024/09/28
# ==============================

import cv2
import numpy as np

class ImageAnalyzer:
    def __init__(self):
        self.img = []
        self.has_fire = False
        self.fire_image_coordinate = [] # 着火点在图像上的坐标
        self.fire_real_coordinate = [] # 着火点在现实中的位置，通过比例尺将图像上的坐标转换成现实坐标
        self.ruler = 0 # 比例尺， 表示图上一个像素对应现实中的长度（单位：cm）

    # 设置当前ImageAnalyzer需要分析的image
    def set_image(self, img):
        self.img = img

    # 函数用于查看当前img中是否有着火点，如果有，返回True并更新self.fire_image_coordinate
    # 否则，返回False
    def fire_detect(self):
        has_fire = False
        if has_fire:
            self.has_fire = True
            # 更新self.fire_image_coordinate坐标
        else :
            return False

    # 函数用于使用比例尺将着火点在图片上的坐标转换成现实中的坐标
    # 没有输入，输出现实坐标
    def get_real_coordinate(self):
        return self.fire_real_coordinate

