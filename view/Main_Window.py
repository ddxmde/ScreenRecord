from ui.Main_UI import Ui_main_window
from PyQt5.QtGui import QBrush, QColor, QCursor, QPainter, QPainterPath
from PyQt5.QtCore import QRectF, Qt
from PyQt5 import QtCore


class Main_Window(Ui_main_window):

    def __init__(self, parent=None):
        super(Main_Window, self).__init__()

        self.setupUi(self)
        # 窗口边框
        self.border_width = 1
        # 窗口可移动标志
        self.m_flag = False
        # 窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 窗口无窗体
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        QtCore.QMetaObject.connectSlotsByName(self)

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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos()-self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos()-self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 重写鼠标移入事件
    def enterEvent(self, event):
        self.setCursor(Qt.SizeAllCursor)
