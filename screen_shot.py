# ==============================
# Describe:      后台自动定时截屏
# D&P Author:             刘语馨
# Environment:    Python   3.11
# Create Date:       2024/09/24
# ==============================
 
import os
from PIL import ImageGrab
import time
import cv2
import unittest
import threading

class ScreenShooter:
    def __init__(self):
        self.BASE_DIR = os.getcwd() # 得到当前文件目录
        self.dir_name = "screenshots" # 截图文件存放在一个名为screenshots的文件夹中
        self.dir_path = os.path.join(self.BASE_DIR, self.dir_name) # 连接两个目录名成为新的目录名
        self.left = 0 # 左上角的坐标和需要截图的大小
        self.top = 0
        self.width = 0
        self.height = 0
        self.time_image_tuple = () # 一个tuple，保留最新得到的截图信息和它对应的时间
        # =============
        # 选择只使用一个tuple保存新的的原因很简单，我们需要监测火情，而不是储存数据
        # 因此只需要保存最新的图片即可，监测和图片分析函数会自动分析最新图片的数据，确保在着火的第一时间能够察觉
        # =============
        self.stop = True # 初始状态下的trigger表示停止

    def stop_shooter(self):
        if self.stop:
            print("shooter already stopped.")
        else:
            self.stop = True

    def start_shooter(self):
        if not self.stop:
            print("shooter already started.")
        else:
            self.stop = False

    # 设置截屏区域的左上角坐标和宽高
    # 单位：像素
    def set_region(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def get_shots(self, time_elapse):
            while True:
                if not self.stop:
                    if not os.path.exists(self.dir_path):
                        os.mkdir(self.dir_path)
                    # 获取当前时间
                    current_time = time.localtime()
                    # 格式化时间
                    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
                    # 使用imageGrab函数截取屏幕区域
                    screenshot = ImageGrab.grab((self.left, self.top, self.left + self.width, self.top + self.height))
                    # 保存截图到文件
                    file_name = "latest_shoot.png"
                    file_path = os.path.join(self.dir_path, file_name)
                    screenshot.save(file_path)
                    print(f"截图已保存到'{file_path}'")
                    # 将截图信息保存到time_image_tuple中
                    # 其中img是一个像素矩阵
                    img = cv2.imread(file_path)
                    self.time_image_tuple = (formatted_time, img)
                    # 等待1秒
                    time.sleep(time_elapse)
                else:
                    break
            print("截图已停止")

class ShoterTest(unittest.TestCase):
    def test_not_start(self):
        new_shooter = ScreenShooter()
        new_shooter.get_shots(1)

    def test_shooter(self):
        new_shooter = ScreenShooter()
        new_shooter.set_region(300, 0, 500, 500)
        new_shooter.start_shooter()
        # 设置一个线程进行截图工作
        # 将这个线程的target设置为get_shots，并传参
        shoot_thread = threading.Thread(target=new_shooter.get_shots, args=(1, ))
        shoot_thread.start() # 启动线程
        # 主线程中设置一段时间
        time.sleep(5)
        # 停止shooter
        new_shooter.stop_shooter()
        print(new_shooter.time_image_tuple)
        print(new_shooter.time_image_tuple[1].shape)
        cv2.imshow('NewWindow', new_shooter.time_image_tuple[1])


