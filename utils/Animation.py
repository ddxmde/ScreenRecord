#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-18 18:16:00
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0


from PyQt5.QtCore import QPropertyAnimation, QSize

class Animation():
    @staticmethod
    def showBySize(target,duration):
        width,height = target.width(),target.height()
        #print(width, height)
        animation = QPropertyAnimation(target, b'size', target)
        animation.setStartValue(QSize(0, 0))  # 设置起始点
        animation.setEndValue((QSize(width, height)))  # 设置终点
        animation.setDuration(duration)  # 时长单位毫秒
        animation.start()
        target.show()

    @staticmethod
    def closeBySize(target, duration):
        width, height = target.width(), target.height()
        #print(width, height)
        animation = QPropertyAnimation(target, b'size', target)
        animation.setStartValue(QSize(width, height))  # 设置起始点
        animation.setEndValue((QSize(0,0)))  # 设置终点
        animation.setDuration(duration)  # 时长单位毫秒
        animation.start()
        target.close()
