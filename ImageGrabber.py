import win32gui
import win32ui
from ctypes import windll
from PIL import Image
from time import sleep, time
import cv2
import numpy as np

class ImageGrabber:

    def __init__(self, windowName):
        self.windowName = windowName
        self.hookWindow()
        return

    def hookWindow(self):
        self.hwnd = win32gui.FindWindow(None, self.windowName)
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        self.w = right - left
        self.h = bot - top
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()
        return

    def getImage(self):
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)
        self.saveDC.SelectObject(saveBitMap)
        result = windll.user32.PrintWindow(
            self.hwnd, self.saveDC.GetSafeHdc(), 0)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        return im

    def getNPImg(self):
        img = self.getImage()
        return cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2BGR)

    def unhookWindow(self):
        self.saveDC.DeleteDC()
        self.mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwndDC)
        return


def current_milli_time(): return int(round(time() * 1000))


def teste():
    obj = ImageGrabber('Windowed Projector (Source) - Tibia')
    im1 = obj.getImage()
    im1.save('TesteIM1.jpg')
    sleep(3)
    im2 = obj.getImage()
    im2.save('TesteIM2.jpg')
    obj.unhookWindow()
    end_time = current_milli_time()


if __name__ == '__main__':
    teste()
