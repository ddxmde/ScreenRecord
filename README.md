# 截图小工具



## 类库使用

PyQt5 

更多详见 [requirement.txt](./requirement.txt)

## 功能项

- 全屏录制 
- 窗口录制
- 设置
  - 选择存储位置
  - 选择保存格式
- 退出

![](./demo/1.jpg)

![](./demo/2.jpg)

## 项目目录

- assets -- 资源目录
  - img -- 图片资源
  - icons.py -- icons.qrc生成的py文件
  - icons.qrc -- 资源文件
- components -- 组件目录
  - LabelButton.py -- 自定义按钮标签组件
  - Menu.py -- 菜单栏
  - Setting.py -- 设置栏
- ui -- 基础ui目录
  - Main_ui.py -- Main_UI.ui生成的py文件（主窗口）
  - Record_Window.py -- Record_Window.ui生成的（录制窗口）
- utils -- 处理工具
  - record.py -- 处理录制程序
  - Animation.py -- 动画处理程序
- view -- 视图目录
  - Main_View.py -- 主程序视图
  - Main_Window.py -- 基础窗口视图
  - Record_View.py -- 录制窗口视图
- main.py -- 程序入口

P.S.继承关系

Main_Window.py 继承于 Main_ui.py

Menu.py 和 Setting.py 继承于 Main_Window.py

Main_View.py 继承上面的两个组件

Record_View.py 继承于 Record_Window.py



