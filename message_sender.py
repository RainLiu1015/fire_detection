# ==================================
# Describe:使用serverchan推送消息到手机
# D&P Author:                  刘语馨
# Environment:         Python   3.11
# Create Date:            2024/10/09
# ==================================

from serverchan_sdk import sc_send
import unittest
import requests
from imgurpython import ImgurClient
import pyimgur
import os
import json


CLIENT_ID = '59278a7c4fc9396'
CLIENT_SECRET = 'a76cb05edba10f1a167af8b013cf6ebdfe767ae9'
client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
current_dir = os.getcwd()
IMAGE_PATH = current_dir + '/screenshots/latest_shoot.png'
KEY = 'sctp2487tk8pqyjzgs2hwvjaqhvhtha'


class MessageSender:
    def __init__(self):
        self.key = KEY

    # 用于生成一条报警信息
    def generate_alarm(self, x, y, object):
        return "在您的房间中坐标为：("+str(x)+","+str(y)+")的位置有疑似火情，高温物体疑似为"+object+", 请您注意！"

    def serverchan_send_alarm(self, x, y, object):
        tag = "火情报警"
        title = "一条新的火情警报！！🚨"
        desp = self.generate_alarm(x, y, object)
        # 接下来将图片上传到图床并且获取url链接
        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(IMAGE_PATH, title="Uploaded with PyImgur")
        image_url = uploaded_image.link
        print(image_url)
        desp = desp + '这是摄像头截图：![image]({' + image_url + '})'
        response = sc_send(self.key, title, desp, {"tags": tag})
        if response['message'] == 'SUCCESS':
            print("message sent. ")
        else :
            print(response)

    def wx_send_alarm(self, x, y, object):
    # 只有在win系统中可以适用
        # wx = WeChat()
        # wx.GetSessionList()
        # msg = self.generate_alarm(x, y, object)
        # who = '文件传输助手'
        # files = [IMAGE_PATH]
        # wx.SendMsg(msg, who)
        # wx.SendFiles(filepath=files, who=who)
        # msgs = wx.GetAllMessage(savepic=True)
        return

class test(unittest.TestCase):
    def test1(self):
        sc_send(KEY, "图片测试",
                        "来自互联网的图片：![客厅](https://pic3.zhimg.com/80/v2-c3f01818baf79845d950940059866f80_1440w.webp)",
                        {"tags": 'tag1|tag2'})
    #     # 似乎只能发送来自互联网的图片，这一点很难办哇
    def test_serverchan_send_alarm(self):
        MS = MessageSender()
        MS.serverchan_send_alarm(10, 15, '书本')

    #
    # def test2(self):
    #     MS = MessageSender("sctp2487tk8pqyjzgs2hwvjaqhvhtha")
    #     MS.send_message("图片测试",
    #                     "来自本地的图片：![客厅](/Users/apple/Desktop/1.jpg)",
    #                     ["测试"])
    #
    # def test3(self):
    #     MS = MessageSender("sctp2487tk8pqyjzgs2hwvjaqhvhtha")
    #     MS.fire_alarm(100, 20, '书本')
    #
    # def test4(self):
    #     # 测试image upload
    #     MS = MessageSender("sctp2487tk8pqyjzgs2hwvjaqhvhtha")
    #     MS.image_upload('/Users/apple/Desktop/1.jpg')
    def test_smms_upload(self):
        headers = {'Authorization': 'yMHlnFebeSlTCrrGttbbu2vl3VFXLPrI'}
        files = {'smfile': open(IMAGE_PATH, 'rb')}
        url = 'https://sm.ms/api/v2/upload'
        res = requests.post(url, files=files, headers=headers).json()
        print(json.dumps(res, indent=4))