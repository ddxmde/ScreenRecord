#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-18 16:49:28
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

import sys
from view.Main_View import Main_View
from PyQt5.QtWidgets import QApplication
import pynput




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main_View()
    win.show()
    sys.exit(app.exec_())
