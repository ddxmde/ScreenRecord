#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-18 17:11:10
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
from components.Menu import Menu
from components.Setting import Setting
from view.Record_View import Record_View
import assets.icons
import os,sys

def check_path():
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return application_path

class Main_View(QWidget, Menu, Setting):
    def __init__(self):
        #print("初始化Main_View")
        super(Main_View, self).__init__()
        
        QtCore.QMetaObject.connectSlotsByName(self)
        #self.success_block_widget.close()
        #self.setting_block_widget.close()

        # 设置文件保存路径
        
        self.save_path = check_path()
        self.setting_save_label.setText("保存位置："+self.save_path)
        # 文件保存类型
        self.save_type = 0 # 0-mp4 1-png 2-gif
        self.save_types = ["mp4","png","gif"]

        # 程序运行状态
        self.recording = False # 默认未运行

        # 是否录制声音
        self.record_sound = False # 默认是

        # 录制对象 0-屏幕 1-窗口
        self.record_target = 0 # 默认屏幕
        self.menu_full_button.setSrc(":img/screen1.png")

        # 录制窗口
        self.record_window = Record_View()
        # 录制窗口始终置顶
        self.record_window.setWindowFlags(
            self.record_window.windowFlags() | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.record_window.close()


    def set_result_tip(self,icon,text):
        self.success_button.setSrc(icon)
        self.label_11.setText(text)

    def keyPressEvent(self, QKeyEvent):  # 键盘某个键被按下时调用
        if QKeyEvent.modifiers() == Qt.ControlModifier and QKeyEvent.key() == Qt.Key_C:
            pass
    
