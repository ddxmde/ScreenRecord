#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-19 00:11:25
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

import os
from PIL import ImageGrab
import numpy as np
import cv2
import datetime
import imageio
import time
import math
from moviepy.editor import *
import threading

class Record_save_Thread(threading.Thread):
    def __init__(self, target,video,video_file):  # 通过初始化赋值的方式实现UI主线程传递值给子线程
        super(Record_save_Thread, self).__init__()
        self.target = target
        self.video = video
        self.video_file = video_file

    def run(self):
        #print("线程开始")
        self.target.video_list.append(
            self.target.save_video(self.video, self.target.img_list, self.video_file))
        self.target.img_list = []
        #print(self.target.video_list)
        #self.my_signal.emit(len(self.target.video_list))

class Record_Utils():
    def __init__(self):
        self.isalive = True
        self.img_list = []
        self.video_list = []
        self.count = 0
        self.save_video_path = ""
        self.fps = 30
        self.thread_pool = []
    def stop(self):
        self.isalive = False

    def record(self, pos, size, fps, type, save_path):
        if type == "gif":
            self.recordGif(pos, size, fps, type, save_path)
        elif type == "png":
            self.recordPng(pos,size,type,save_path)
        else:
            self.recordVideo(pos,size, fps, type, save_path)

    def recordPng(self,pos,size,type,save_path):
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"."+type
        file_with_path = save_path + "\\" + filename

        bbox = (pos[0], pos[1], size[0], size[1])
        im = ImageGrab.grab(bbox)
        im.save(file_with_path)

    def recordVideo(self,pos,size,fps,type,save_path):
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"."+type
        file_with_path = save_path + "\\" + filename
        self.save_video_path = file_with_path
        self.fps = fps
        if type == "mp4":
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        else:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')

        bbox = (pos[0], pos[1], size[0], size[1])
        #im = ImageGrab.grab(bbox)
        #im.show()
        while self.isalive:
            # 四个参数代表了开始截图的x,y，结束截图的x,y，后两个可以看电脑
            #for i in range(fps):
            #print(datetime.datetime.now())
            im = ImageGrab.grab(bbox)
            self.img_list.append(im)
            if len(self.img_list) > 2*fps:
                tmp_video_file = save_path + "\\" + str(datetime.datetime.now().strftime(
                    "%Y%m%d%H%M%S"))+"#"+str(self.count)+"."+type
                video = cv2.VideoWriter(tmp_video_file, fourcc, fps, size)
                video_save_thread = Record_save_Thread(self, video,tmp_video_file)
                video_save_thread.start()
                self.thread_pool.append(video_save_thread)
                self.count += 1
            #time.sleep(math.ceil(1000/fps)/1000)

        if len(self.img_list) > 0:
            tmp_video_file = save_path + "\\" + str(datetime.datetime.now().strftime(
                "%Y%m%d%H%M%S"))+"#"+str(self.count)+"."+type
            video = cv2.VideoWriter(
                tmp_video_file, fourcc, fps, size)
            video_save_thread = Record_save_Thread(self, video, tmp_video_file)
            video_save_thread.start()
            self.thread_pool.append(video_save_thread)
        for t_d in self.thread_pool:
            t_d.join()
        L = []
        for filePath in self.video_list:
            video = VideoFileClip(filePath)
            L.append(video)
        
        final_clip = concatenate_videoclips(L)
            # 生成目标视频文件
        final_clip.to_videofile(self.save_video_path, fps=self.fps, remove_temp=True)
        for filePath in self.video_list:
            os.remove(filePath)
        self.video_list =[]
        self.img_list = []
        L=[]
        #print("完成拼接")

    def save_video(self, video, imgs, video_file):
        self.img_list = []
        #print("处理"+str(len(imgs))+"张")
        for im in imgs:
            frame = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
            video.write(frame)
        video.release()
        #self.video_list.append(video_file)
        return video_file

    def recordGif(self, pos, size, fps, type, save_path):
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"."+type
        file_with_path = save_path + "\\" + filename
        bbox = (pos[0], pos[1], size[0], size[1])
        frames = []

        while self.isalive:
            _before = datetime.datetime.now()
            # 四个参数代表了开始截图的x,y，结束截图的x,y，后两个可以看电脑
            for i in range(fps):
                im = ImageGrab.grab(bbox)
                frames.append(im)
                time.sleep(math.ceil(1000/fps)/1000)
                # _after = datetime.datetime.now()
                # while (_after-_before).seconds < math.ceil(1000/fps):
                #     _after = datetime.datetime.now()
        imageio.mimsave(file_with_path, frames, 'GIF', duration=1/fps)
