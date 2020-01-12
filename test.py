import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import time


def current_milli_time(): return int(round(time.time() * 1000))


start_time = current_milli_time()
hwnd = win32gui.FindWindow(None, 'Tibia')

# Change the line below depending on whether you want the whole window
# or just the client area.
# left, top, right, bot = win32gui.GetClientRect(hwnd)
left, top, right, bot = win32gui.GetWindowRect(hwnd)
w = right - left
h = bot - top

hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

saveDC.SelectObject(saveBitMap)

# Change the line below depending on whether you want the whole window
# or just the client area.
# result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)

im = Image.frombuffer(
    'RGB',
    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    bmpstr, 'raw', 'BGRX', 0, 1)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hwnd, hwndDC)
end_time = current_milli_time()

if result == 1:
    # PrintWindow Succeeded
    pix = im.load()
    print(pix[1372, 316] == pix[1373, 316])
    im.save("test.bmp")

print("{0}".format(end_time-start_time))
