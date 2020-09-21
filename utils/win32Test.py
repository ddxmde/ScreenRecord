#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-19 20:40:36
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

#coding=utf-8
import threading
import win32gui
import win32process
import psutil
from tkinter import *
root = Tk()
s = StringVar()


def active_window_process():
    try:
        pid = win32process.GetWindowThreadProcessId(
            win32gui.GetForegroundWindow())
            
        return(psutil.Process(pid[-1]))
    except:
        pass


def to_label():
    global s
    while True:
        app_window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(app_window)
        clssname = win32gui.GetClassName(app_window)
        print(title)
        print(type(clssname))
        #print(app_window)
        s.set(active_window_process().name)
    return


Label(root, textvariable=s).pack()
if __name__ == "__main__":
    t = threading.Thread(target=to_label)
    t.start()
    root.mainloop()
