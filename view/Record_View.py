#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-18 22:05:02
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0



from PyQt5.QtCore import QPoint, Qt
from ui.Record_Window import Ui_Record_Window
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QBrush, QColor, QPainter, QPainterPath
from PyQt5.QtCore import QRectF, Qt
from PyQt5 import QtCore

class Record_View(QDialog,Ui_Record_Window):
    def __init__(self,parent=None):
        #print("初始化Message_Notice_View")
        super(Record_View, self).__init__()
        self.setupUi(self)
        # 窗口边框
        self.border_width = 5
        # 窗口可移动标志
        self.m_flag = False
        # 窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 窗口无窗体
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        QtCore.QMetaObject.connectSlotsByName(self)

        self._initDrag()  # 设置鼠标跟踪判断扳机默认值
        self.setMouseTracking(True)  # 设置widget鼠标跟踪


    def _initDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False


    def paintEvent(self, event):
    	# 阴影
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        pat = QPainter(self)
        pat.setRenderHint(pat.Antialiasing)
        pat.fillPath(path, QBrush(Qt.white))

        color = QColor(0, 0, 0, 60)

        for i in range(10):
            i_path = QPainterPath()
            i_path.setFillRule(Qt.WindingFill)
            ref = QRectF(10-i, 10-i, self.width()-(10-i)
                         * 2, self.height()-(10-i)*2)
            # i_path.addRect(ref)
            i_path.addRoundedRect(ref, self.border_width, self.border_width)
            color.setAlpha(150 - i**0.5*50)
            pat.setPen(color)
            pat.drawPath(i_path)

        # 圆角
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.Antialiasing)  # 抗锯齿
        pat2.setBrush(Qt.white)
        pat2.setPen(Qt.transparent)

        rect = self.rect()
        rect.setLeft(1)
        rect.setTop(1)
        rect.setRight(1)
        rect.setBottom(1)
        rect.setWidth(rect.width()-2)
        rect.setHeight(rect.height()-2)
        pat2.drawRoundedRect(rect, 4, 4)

    def resizeEvent(self, QResizeEvent):
        # 自定义窗口调整大小事件
        # 改变窗口大小的三个坐标范围
        self._right_rect = [QPoint(x, y) for x in range(self.width() - 15, self.width() + 15)
                            for y in range(self.widget.height() + 20, self.height() - 15)]
        self._bottom_rect = [QPoint(x, y) for x in range(10, self.width() - 15)
                             for y in range(self.height() - 15, self.height() + 10)]
        self._corner_rect = [QPoint(x, y) for x in range(self.width() - 15, self.width() + 10)
                             for y in range(self.height() - 15, self.height() + 10)]

    def mousePressEvent(self, event):
        # 重写鼠标点击的事件
        if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
            # 鼠标左键点击右下角边界区域
            self._corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
            # 鼠标左键点击右侧边界区域
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
            # 鼠标左键点击下侧边界区域
            self._bottom_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.y() < self.widget.height()):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        # 判断鼠标位置切换鼠标手势
        if QMouseEvent.pos() in self._corner_rect:  # QMouseEvent.pos()获取相对位置
            self.setCursor(Qt.SizeFDiagCursor)
        elif QMouseEvent.pos() in self._bottom_rect:
            self.setCursor(Qt.SizeVerCursor)
        elif QMouseEvent.pos() in self._right_rect:
            self.setCursor(Qt.SizeHorCursor)

        # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
        # 没有定义左方和上方相关的5个方向，主要是因为实现起来不难，但是效果很差，拖放的时候窗口闪烁，再研究研究是否有更好的实现
        if Qt.LeftButton and self._right_drag:
            # 右侧调整窗口宽度
            self.resize(QMouseEvent.pos().x(), self.height())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._bottom_drag:
            # 下侧调整窗口高度
            self.resize(self.width(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._corner_drag:
            #  由于我窗口设置了圆角,这个调整大小相当于没有用了
            # 右下角同时调整高度和宽度
            self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._move_drag:
            # 标题栏拖放窗口位置
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        # 鼠标释放后，各扳机复位
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False
        print(self.width(),self.height())
        print(self.record_frame.width(),self.record_frame.height())
    # 重写鼠标移入事件
    def enterEvent(self, event):
        self.setCursor(Qt.SizeAllCursor)
