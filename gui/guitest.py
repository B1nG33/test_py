import win32gui
import pyautogui
import subprocess
import time

#  操作等待1s
pyautogui.PAUSE = 1
#  防故障
pyautogui.FAILSAFE = False

# 打开软件
subprocess.Popen(["C:/MAKER\PIFLOW/3.2.143.0/bin/PiFlow.exe"])

time.sleep(10)

# 获取窗口句柄
hwndmain = win32gui.FindWindow("QMainWindow", "PiFlow")
# hwnd1 = win32gui.FindWindow("QDialog", "选择工作目录")

# 定义函数：传入图片，在窗口找到对应位置并点击

def click_image(image_name):
    image_path = f"{image_name}.png"
    button_location = pyautogui.locateOnScreen(image_path)
    button_center = pyautogui.center(button_location)
    pyautogui.click(button_center)

click_image("新建工程")

handle1 = win32gui.FindWindow("QDialog", "新建工程")

# click_image("浏览")

# # 新建文件夹
# pyautogui.hotkey('ctrl', 'shift', 'n')
# pyautogui.typewrite('test')
# pyautogui.press('enter')
# pyautogui.press('enter')
# time.sleep(1)
#
# click_image("选择文件夹")
#
# click_image("新建")
#
# click_image("导入模型")
#
# click_image("")








