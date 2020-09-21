#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-21 18:05:13
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

import os
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qt import Qt


class LabelTextButton(QLabel):
    # 自定义单击信号
    clicked = pyqtSignal()
    # 自定义双击信号
    DoubleClicked = pyqtSignal()
    # 自定义鼠标移入信号
    moveIn = pyqtSignal()
    # 自定义鼠标移除
    moveOut = pyqtSignal()

    def __init__(self, target, text):
        super(LabelTextButton, self).__init__(parent=target)
        self.setText(text)
    
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
    def leaveEvent(self, event):
        self.moveOut.emit()
