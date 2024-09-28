# ==============================
# Describe:      分析图像并识别物体
# D&P Author:             刘语馨
# Environment:    Python   3.11
# Create Date:       2024/09/28
# 备注：可以考虑使用现成的cv模型的api
# ==============================

import cv2
class ObjectRecognizer:
    def __init__(self):
        self.img = []

    # 设置当前ObjectRecognizer需要分析的image
    def set_image(self, img):
        self.img = img

    # 根据输入的坐标（像素）得到当前位置的物体
    def get_object(self, x, y):
        return "桌子"