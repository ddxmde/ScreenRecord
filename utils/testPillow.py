#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-19 19:02:52
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

import os

from PIL import ImageGrab

import time

import datetime


def grab_and_save_mpg(name, position=None):
    command = "ffmpeg -f gdigrab -framerate 30 -offset_x 100 -offset_y 100 -video_size 920*580 -i desktop {}".format(
        name)
    cmd_proces= os.popen(command)
    _before = datetime.datetime.now()
    while True:
        _after = datetime.datetime.now()
        total_seconds = (_after-_before).seconds
        if total_seconds > 60:
            os.popen("q")
            break

if __name__ == "__main__":
    # images = []
    # _before = datetime.datetime.now()
    # for i in range(100):
    #     #tmp_now0 = datetime.datetime.now()
    #     im = ImageGrab.grab((0,0,900,900))
    #     images.append(im)
    #     #tmp_now = datetime.datetime.now()
    #     #print(str(i)+" 花费时间：%s" % (str((tmp_now-tmp_now0).total_seconds())))
    # _after = datetime.datetime.now()
    # total_seconds = (_after-_before).total_seconds()
    # print("花费时间：%s,平均 %.4f 张/秒" % (str(total_seconds),100/total_seconds))
    grab_and_save_mpg("E:\\tmp.mpg")



