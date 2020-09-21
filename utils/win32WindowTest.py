#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-19 21:14:25
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0
import win32gui
import re
import sys


class WindowMgr():
    '''Encapsulates some calls to the winapi for windows management'''

    def __init__(self):
        '''Constructor'''
        self._handle = None

    def find_window(self, class_name, window_name):
        '''find a window by its window_name'''
        self._handle = win32gui.FindWindow(class_name, window_name)

    def __window_enum_callback(self, hwnd, wildcard):
        '''pass to win32gui.EnumWindows() to check all the opened windows'''
        if re.match(wildcard, str(win32gui.GetWindowsText(hwnd))) != None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self.__window_enum_callback, wildcard)

    def set_foreground(self):
        '''put the window in the forground'''
        win32gui.SetForegroundWindow(self._handle)


def main():
    w = WindowMgr()
    w.find_window_wildcard('.*Hello*.')
    w.set_foreground()


if __name__ == '__main__':
    sys.exit(main())
