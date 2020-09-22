#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-22 01:27:29
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

import datetime
import os
from subprocess import CREATE_NEW_CONSOLE
from sys import path
import win32gui
import sys
from PyQt5.QtWidgets import QApplication
import threading
import subprocess
import math
from PyQt5.QtCore import QThread, pyqtSignal

def check_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS+"\\ffmpeg.exe"
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\ffmpeg.exe"

class Record_Utils:
    def __init__(self):
        self.is_running = False
        self.ffmpeg_process = None
        self.ffmpeg_exe = check_path()

    def record(self, target, pos, size, fps, stype, save_path):
        if stype == "gif":
            self.recordGif(target, pos, size, fps, stype, save_path)
        elif stype == "png":
            self.recordPng(target, pos, size, stype, save_path)
        else:
            self.recordVideo(target, pos, size, fps, stype, save_path)

    def stop(self):
        if self.is_running:
            self.ffmpeg_process.stdin.write("q")
            self.ffmpeg_process.stdin.flush()
            #self.ffmpeg_process.send_signal(signal.CTRL_C_EVENT)
            self.is_running = False


    def recordPng(self, target, pos, size, stype, save_path):
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"."+stype
        file_with_path = save_path + "\\" + filename
        hwnd = win32gui.FindWindow(None, 'desktop')
        #app = QApplication(sys.argv)
        im = QApplication.primaryScreen().grabWindow(
            hwnd, pos[0], pos[1], size[0]-pos[0], size[1]-pos[1]).toImage()
        im.save(file_with_path)

    def recordVideo(self,target,pos,size,fps,stype,save_path):
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"."+stype
        file_with_path = save_path + "\\" + filename
        self.tmp_video_name = file_with_path
        _tmp_width = math.floor((size[0]-pos[0]) / 32) * 32
        _tmp_height = math.floor((size[1]-pos[1]) / 2) * 2
        print(pos, _tmp_width, _tmp_height)
        if target == 0:
            # 全屏
            _cmd = check_path()+" -f gdigrab -framerate {fps} -i desktop -s {width}x{height} -pix_fmt yuv420p -c:v h264 -b:v 2000k {path}".format(
                fps=fps, width=size[0], height=size[1], path=file_with_path)
        else:
            _cmd = check_path()+" -f gdigrab -framerate {fps} -offset_x {x} -offset_y {y} -video_size {width}x{height} -i desktop -pix_fmt yuv420p -c:v libx264 {path}".format(
                fps=fps,  x=pos[0], y=pos[1], width=_tmp_width, height=_tmp_height, path=file_with_path)

        self.is_running = True
        self.ffmpeg_process = subprocess.Popen(
            _cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
            universal_newlines=True)
        self.ffmpeg_process.wait()

    def recordGif(self, target, pos, size, fps, stype, save_path):
        #self.ffmpeg_process.wait()
        # _tmp_thread = threading.Thread(target=self.recordVideo, args=[
        #                                target, pos, size, fps, "mp4", save_path,])

        # _tmp_thread.start()
        # _tmp_thread.join()
        self.recordVideo(target, pos, size, fps, "mp4", save_path)
        gif_name = "".join(self.tmp_video_name.split(".")[:-1])+"."+stype
        if self.tmp_video_name is None:
            return
        #  -vf scale=360:-1
        _cmd = check_path()+" -i {video_path} {gif_path}".format(
            video_path=self.tmp_video_name,
            gif_path=gif_name)
        _tmpproces = subprocess.Popen(_cmd, shell=False, universal_newlines=True)
        _tmpproces.wait()
        if os.path.exists(self.tmp_video_name):
            os.remove(self.tmp_video_name)
            self.tmp_video_name = None
        #print("gif制作完成")
            

