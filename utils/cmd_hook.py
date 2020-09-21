#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-19 23:08:54
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

import os
import subprocess
import threading
from datetime import datetime
import time
import signal
import shlex
class Shell_Object(object):
    

    def __init__(self,command=''):
        super(Shell_Object,self).__init__()
        self.process = subprocess.Popen(
            command, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True)
        self.current_result = {}
    
    def is_waitting(self):
        if self.process.poll() is None:
            return True
        else:
            return False

    def get_cur_result(self):
        # 获取最新的执行结果并返回
        result =  self.current_result
        self.current_result = {}
        return result

    def result_monitor(self):
        while True:
            _waitting = self.is_waitting()
            if not _waitting:
                out, err = self.process.communicate()
                self.current_result['out']=out
                self.current_result['error'] = err
                break

    def close(self,Force=False):
        # 关闭shell - 如果正在执行，则返回False，成功关闭返回True
        if Force:
            self.process.kill()
            return True
        else:
            if self.is_waitting() is not None:
                self.process.kill()
                return True
            else:
                return False

    def execute_or_not(self, command,require_result=False,timeout=None):
        # 返回True正在执行 返回False未执行
        if timeout is None:
            if self.is_waitting():
                print("is waitting")
                return False
        else:
            _waitting = self.is_waitting()
            _before = datetime.now()
            while _waitting:
                _after = datetime.now()
                if ((_after-_before).total_seconds()*1000>timeout):
                    print("已经超时")
                    return False
                _waitting = self.is_waitting()
        self.process.stdin.writelines(command)
        if require_result:
            _t = threading.Thread(target=self.result_monitor)
            _t.start()
            print("开启线程执行")
        return True


if __name__ == "__main__":  
    try:
        shell_cmd = 'ffmpeg.exe -f gdigrab -framerate 30 -offset_x 100 -offset_y 100 -video_size 920*580 -i desktop "rtt.mp4"'
        cmd = shlex.split(shell_cmd)
        p = subprocess.Popen(
            cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # count = 0
        while p.poll() is None:
            line = p.stdout.readline().decode('gbk').strip()
            print(line)
            # count += 1
            # if count == 50:
            #     os.kill(0, signal.CTRL_C_EVENT)
        # if p.returncode == 0:
        #     print('subprocess success')
        # else:
        #     print('subprocess failed with code', p.returncode)
        time.sleep(10)
        os.kill(0, signal.CTRL_C_EVENT)
    except (OSError, ValueError, KeyboardInterrupt):
        print('stop here')

