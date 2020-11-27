import keyboard
import PIL.ImageGrab
import time
import pyperclip
import pytesseract
from playsound import playsound
import win32gui
import win32api
import pyautogui
directory = r"C:\Users\snir\OneDrive\Desktop\files\\"
playsound(directory + "startup.wav", block = False)
print("press ctrl, then for english press ctrl again, shift for hebrew and alt for arabic")
first_key = keyboard.read_key()
while first_key != "ctrl":
    first_key = keyboard.read_key()
    print("waiting for the keys")
playsound(directory + "first_click.wav", block=False)
print(first_key, "pressed (first key)")
firstx, firsty = pyautogui.position()
time.sleep(0.3)
second_key = keyboard.read_key()
while second_key != "ctrl" and second_key != "alt" and second_key != "shift":
    second_key = keyboard.read_key()
    print("waiting for the keys")
print(second_key, "pressed (second key)")
playsound(directory + "second_click.wav", block=False)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
dc = win32gui.GetDC(0)
red = win32api.RGB(255, 0, 0)
x, y = pyautogui.position()
try:
    im = PIL.ImageGrab.grab(bbox=(firstx, firsty, x, y))
except:
    im = PIL.ImageGrab.grab(bbox=(x, y, firstx, firsty))
for num1 in range(35):
    for num in range(firsty, y):
        win32gui.SetPixel(dc, firstx - 1, num, red)
        win32gui.SetPixel(dc, firstx - 2, num, red)
        win32gui.SetPixel(dc, x + 1, num, red)
        win32gui.SetPixel(dc, x + 2, num, red)
    for num in range(firstx - 2, x + 2):
        win32gui.SetPixel(dc, num, firsty + 1, red)
        win32gui.SetPixel(dc, num, firsty, red)
        win32gui.SetPixel(dc, num, y, red)
        win32gui.SetPixel(dc, num, y - 1, red)
lang = ""
if second_key == "ctrl":
    lang = "eng"
    print("language: eng")
elif second_key == "shift":
    lang = "heb"
    print("language: hebrew")
else:
    lang = "ara"
    print("language: arabic")
try:
    x = pytesseract.image_to_string(im, lang=lang).strip()
    print("the clipboard:", x)
    if len(x) < 5:
        raise Exception
except Exception as e:
    playsound(directory + "negativebeep.wav", block=False)
    time.sleep(1)
    hwnd = win32gui.WindowFromPoint((0, 0))
    monitor = (0, 0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
    win32gui.InvalidateRect(hwnd, monitor, True)
    time.sleep(1)
    if len(str(e)) == 0:
        print("cant get the text from the image")
    else:
        print("the error:", e)
    quit()
pyperclip.copy(x)
playsound(directory + "success.wav", block=False)
time.sleep(0.5)
hwnd = win32gui.WindowFromPoint((0, 0))
monitor = (0, 0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
win32gui.InvalidateRect(hwnd, monitor, True)
time.sleep(2.5)
quit()
