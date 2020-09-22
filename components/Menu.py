#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-18 16:51:47
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

import sys
from PyQt5 import QtCore
from PyQt5.QtCore import  QThread, pyqtSignal,Qt
from PyQt5.QtWidgets import QApplication
from view.Main_Window import Main_Window
from components.LabelButton import LabelButton
from utils.Animation import Animation
from utils.FFmpegRecord import Record_Utils

class Record_Thread(QThread):
    finish_record = pyqtSignal()
    def __init__(self,target, pos, size, fps, type, save_path):  # 通过初始化赋值的方式实现UI主线程传递值给子线程
        super(Record_Thread, self).__init__()
        self.pos = pos
        self.size = size
        self.fps = fps
        self.type = type
        self.save_path = save_path
        self.target = target
    def stop(self,flag):
        self.record_utils.stop()

    def run(self):
        #print("线程开始")
        self.record_utils = Record_Utils()
        self.record_utils.record(self.target,self.pos, self.size, self.fps, self.type, self.save_path)
        #print("线程结束")
        self.finish_record.emit()



        
class Menu(Main_Window):
    def __init__(self,parent=None):
        super(Menu, self).__init__()
        self.menu_ui()
        self.setting_button_open = False

    # play_button clicked
    @QtCore.pyqtSlot()
    def on_menu_play_button_clicked(self):
        if self.recording:
            # self.record_end_time = datetime.datetime.now()
            # print("时间戳"+str((self.record_end_time-self.record_start_time).seconds))
            # self.recording = False
            self.record_thread.stop(self.recording)
            self.menu_play_button.setSrc(":img/play.png")
            self.set_result_tip(":img/transcode1.png", "正在处理数据……")
            self.label.setText("开始")
        else:
            self.recording = True
            self.menu_play_button.setSrc(":img/stop.png")

            self.showMinimized()

            #self.setWindowOpacity(0.2)
            self.set_result_tip(":img/dot-circle1.png", "正在录制")
            self.label.setText("停止")

            r_fps = 25
            # if self.save_type == 2:
            #     r_fps = 5
            r_type = self.save_types[self.save_type]
            #print(r_type)
            r_pos = (0, 0)
            r_size = (0, 0)
            r_save_path = self.save_path
            if self.record_target == 0:
                # 录制屏幕
                screenRect = QApplication.desktop().screenGeometry()
                screenRect_y = screenRect.height()
                screenRect_x = screenRect.width()
                r_size = (screenRect_x, screenRect_y)
                r_target = 0
            else:
                _app_x = self.record_window.x()
                _app_y = self.record_window.y()
                r_pos = (_app_x+18, _app_y+38)
                r_size = (_app_x+self.record_window.width()-18,
                          _app_y+self.record_window.height()-18)
                r_target = 1
            self.record_thread = Record_Thread(r_target,r_pos,r_size,r_fps,r_type,r_save_path)
            # self.record_start_time = datetime.datetime.now()
            self.record_thread.start()
            self.record_thread.finish_record.connect(self.success_record_confirm)
    
    def success_record_confirm(self):
        if self.save_type == 1:
            # 截图
            self.recording = False
            self.menu_play_button.setSrc(":img/play.png")
            self.label.setText("开始")
            #self.setWindowOpacity(1)
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
            self.showNormal()
        self.recording = False
        self.set_result_tip(":img/success.png", "录制成功……")
    
    # menu_full_button clicked
    @QtCore.pyqtSlot()
    def on_menu_full_button_clicked(self):
        if self.recording:
            return
        if self.record_target == 1:
            self.record_window.close()
            self.record_target = 0
            self.menu_window_button.setSrc(":img/window.png")
            self.menu_full_button.setSrc(":img/screen1.png")

    # menu_window_button clicked
    @QtCore.pyqtSlot()
    def on_menu_window_button_clicked(self):
        if self.recording:
            return
        if self.record_target == 0:
            self.record_window.show()
            #self.record_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.record_target = 1
            self.menu_window_button.setSrc(":img/window1.png")
            self.menu_full_button.setSrc(":img/screen.png")
            self.record_sound = False
            self.menu_sound_button.setSrc(":img/sound.png")
        else:
            self.record_window.close()
            self.record_target = 0
            self.menu_window_button.setSrc(":img/window.png")
            self.menu_full_button.setSrc(":img/screen1.png")


    # menu_sound_button clicked
    @QtCore.pyqtSlot()
    def on_menu_sound_button_clicked(self):
        self.set_result_tip(":img/warning.png", "暂不支持音频")
        # if self.recording or self.save_type == 2:
        #     # 如果是gif保存
        #     return
        # if self.record_sound:
        #     # 录制声音-关闭
        #     self.record_sound = False
        #     self.menu_sound_button.setSrc(":img/sound.png")
        # else:
        #     # 录制声音-打开
        #     self.record_sound = True
        #     self.menu_sound_button.setSrc(":img/sound1.png")

    # menu_setting_button clicked
    @QtCore.pyqtSlot()
    def on_menu_setting_button_clicked(self):
        Animation.showBySize(self.success_block_widget, 3000)
        # if self.setting_button_open:
        #     self.menu_setting_button.setSrc(":img/setting.png")
        #     Animation.closeBySize(self.setting_block_widget, 1000)
        #     self.setting_button_open = False
        #     self.resize(370, 110)
        # else:
        #     self.menu_setting_button.setSrc(":img/setting1.png")
        #     Animation.showBySize(self.setting_block_widget, 3000)
        #     self.setting_button_open = True

    # menu_close_button clicked
    @QtCore.pyqtSlot()
    def on_menu_close_button_clicked(self):
        if self.recording:
            self.set_result_tip(":img/warning.png", "请先结束录制")
        else:
            sys.exit(0)

    def menu_ui(self):
        self.menu_play_button = LabelButton(
            self.menu_play_widget, ":img/play.png")
        self.menu_full_button = LabelButton(
            self.menu_full_widget, ":img/screen.png")
        self.menu_window_button = LabelButton(
            self.menu_window_widget, ":img/window.png")
        self.menu_sound_button = LabelButton(
            self.menu_sound_widget, ":img/sound.png")
        self.menu_setting_button = LabelButton(
            self.menu_setting_widget, ":img/setting1.png")
        self.menu_close_button = LabelButton(
            self.menu_close_widget, ":img/exit.png")
        
        self.menu_play_button.setObjectName("menu_play_button")
        self.menu_full_button.setObjectName("menu_full_button")
        self.menu_window_button.setObjectName("menu_window_button")
        self.menu_sound_button.setObjectName("menu_sound_button")
        self.menu_setting_button.setObjectName("menu_setting_button")
        self.menu_close_button.setObjectName("menu_close_button")

    def keyPressEvent(self, QKeyEvent):  # 键盘某个键被按下时调用
        if QKeyEvent.modifiers() == Qt.ControlModifier and QKeyEvent.key() == Qt.Key_C:
            pass
        if QKeyEvent.modifiers() == Qt.ControlModifier and QKeyEvent.key() == Qt.Key_Q:  # 两键组合
            #modifiers()   判断修饰键
            #Qt.NoModifier   没有修饰键
            #Qt.ShiftModifier    Shift键被按下
            #Qt.ControlModifier    Ctrl键被按下
            #Qt.AltModifier      Alt键被按下
            print('按下了Ctrl-Q键')
            if self.recording:
                #self.record_end_time = datetime.datetime.now()
                #print("时间戳"+str((self.record_end_time-self.record_start_time).seconds))
                self.recording = False
                self.record_thread.stop(self.recording)
                self.menu_play_button.setSrc(":img/play.png")
                self.set_result_tip(":img/transcode1.png", "正在处理数据……")
                self.label.setText("开始")
                self.showNormal()
                if self.record_target == 1:
                    self.record_window.close()
