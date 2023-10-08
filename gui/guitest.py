import pyautogui

button_location = pyautogui.locateOnScreen("create_button.png")
button_center = pyautogui.center(button_location)
pyautogui.click(button_center)