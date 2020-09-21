#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-18 16:52:16
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from view.Main_Window import Main_Window
from components.LabelButton import LabelButton
from components.LabelTextButton import LabelTextButton
import os

class Setting(Main_Window):
    def __init__(self):
        super(Setting, self).__init__()
        self.setting_ui()
        
        #当窗口非继承QtWidgets.QDialog时，self可替换成 None

    # setting_save_button clicked
    @QtCore.pyqtSlot()
    def on_setting_save_button_clicked(self):
        if self.recording:
            return
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            None, "getExistingDirectory", self.save_path)
        #print(len(directory))
        if directory is not None and len(directory)>0:
            self.save_path = directory
            self.setting_save_label.setText("保存位置："+directory)

    # setting_type_mp4_button clicked
    @QtCore.pyqtSlot()
    def on_setting_type_mp4_button_clicked(self):
        if self.recording or self.record_target==1:
            return
        self.init_save_type_icons()
        self.setting_type_mp4_button.setSrc(":img/mp41.png")
        self.save_type = 0

    # setting_type_avi_button clicked
    @QtCore.pyqtSlot()
    def on_setting_type_avi_button_clicked(self):
        self.set_result_tip(":img/warning.png", "暂不支持avi格式")
        # if self.recording or self.record_target == 1:
        #     return
        # self.init_save_type_icons()
        # self.setting_type_avi_button.setSrc(":img/avi1.png")
        # self.save_type = 1

    # setting_type_gif_button clicked
    @QtCore.pyqtSlot()
    def on_setting_type_gif_button_clicked(self):
        if self.recording:
            return
        self.init_save_type_icons()
        self.setting_type_gif_button.setSrc(":img/gif1.png")
        self.save_type = 2
        self.record_sound = False
        self.menu_sound_button.setSrc(":img/sound.png")

    # success_button clicked
    @QtCore.pyqtSlot()
    def on_success_button_clicked(self):
        pass
    
    def init_save_type_icons(self):
        self.setting_type_mp4_button.setSrc(":img/mp4.png")
        self.setting_type_avi_button.setSrc(":img/avi.png")
        self.setting_type_gif_button.setSrc(":img/gif.png")

    #打开文件存储位置
    @QtCore.pyqtSlot()
    def on_setting_save_label_clicked(self):
        #print("打开文件夹")
        os.system("start explorer %s" % self.save_path)

    def setting_ui(self):
        # self.setting_save_widget
        # self.setting_save_label
        # self.setting_type_mp4_widget
        # self.setting_type_avi_widget
        # self.setting_type_gif_widget
        # self.setting_type_widget

        self.setting_save_button = LabelButton(
            self.setting_save_widget, ":img/download.png")

        self.setting_type_mp4_button = LabelButton(
            self.setting_type_mp4_widget, ":img/mp41.png")
        self.setting_type_avi_button = LabelButton(
            self.setting_type_avi_widget, ":img/avi.png")
        self.setting_type_gif_button = LabelButton(
            self.setting_type_gif_widget, ":img/gif.png")
        self.success_button = LabelButton(
            self.success_widget, ":img/dot-circle.png")
        self.label_11.setText("准备就绪……")

        self.setting_save_button.setObjectName("setting_save_button")
        self.setting_type_mp4_button.setObjectName("setting_type_mp4_button")
        self.setting_type_avi_button.setObjectName("setting_type_avi_button")
        self.setting_type_gif_button.setObjectName("setting_type_gif_button")

        self.success_button.setObjectName("success_button")

        
        # 点击文件存储位置标签
        self.setting_save_label = LabelTextButton(
            self.widget_8, "")
        self.setting_save_label.setMinimumSize(QtCore.QSize(300, 35))
        self.setting_save_label.setMaximumSize(QtCore.QSize(300, 35))
        self.setting_save_label.setStyleSheet("color: rgb(68, 68, 68);")
        self.setting_save_label.setObjectName("setting_save_label")
        self.horizontalLayout_2.addWidget(self.setting_save_label)
        # self.setting_save_label.linkActivated.connect(self.save_label_clicked)


