#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-15 18:21:19
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import Qt

class LabelButton(QLabel):
    
    # 自定义单击信号
    clicked = pyqtSignal()
     # 自定义双击信号
    DoubleClicked = pyqtSignal()
    # 自定义鼠标移入信号
    moveIn = pyqtSignal()
    # 自定义鼠标移除
    moveOut = pyqtSignal()

    def __init__(self,target,src,scale=None):
        super(LabelButton,self).__init__(target)
        self.scale = scale
        self.target = target
        self.src = src
        # 设置背景图片
        self.setSrc(src)

    def setSrc(self,src):
        pix = QPixmap(src)
        if self.scale is None:
            pix = pix.scaled(self.target.width(), self.target.height())
        else:
            pix = pix.scaled(self.scale[0], self.scale[1])
        self.setPixmap(pix)
        self.src = src



    # 重写鼠标单击事件
    def mousePressEvent(self, QMouseEvent):  # 单击
        #print("clicked")
        self.clicked.emit()

    # 重写鼠标双击事件
    def mouseDoubleClickEvent(self, e):  # 双击
        self.DoubleClicked.emit()

    # 重写鼠标移入事件
    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        self.moveIn.emit()

    # 重写鼠标移出事件
    def leaveEvent(self,event):
        self.moveOut.emit()
