
#! /usr/bin/env python
# coding=utf-8
 
# ==============================
# Describe:      后台自动定时截屏
# D&P Author:             常成功
# Environment:    Python 2.7.15
# Create Date:       2020/07/07
# ==============================
 
import os
from PIL import ImageGrab
import time

class ScreenShoter:
    def __init__(self):
        self.BASE_DIR = os.getcwd() # 得到当前文件目录
        self.dir_name = "screenshots" # 所有截图文件存放在一个名为screenshots的文件夹中
        self.dir_path = os.path.join(self.BASE_DIR, self.dir_name) # 连接两个目录名成为新的目录名
        self.left = 0 # 左上角的坐标和需要截图的大小
        self.top = 0
        self.width = 0
        self.height = 0

    
    def get_shots(self, time):
        cnt = 0
        try:
            while True:
                if not os.path.exists(self.dir_path):
                    os.mkdir(self.dir_path)
                cnt += 1
                # 使用imageGrab函数截取屏幕区域
                screenshot = ImageGrab.grab((self.left, self.top, self.width, self.height))
                # 保存截图到文件
                file_name = str(cnt) + ".png"
                file_path = os.path.join(self.dir_path, file_name)
                screenshot.save(file_path)
                print(f"截图已保存到'{file_path}'")
                # 等待1秒
                time.sleep(time)
        except KeyboardInterrupt:
            print("截图已停止")
