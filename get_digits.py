from ctypes import *
from ctypes.wintypes import *
import psutil
import win32gui
import win32api
import win32process
import struct
from time import sleep
from ImageGrabber import ImageGrabber



OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle
WriteProcessMemory = windll.kernel32.WriteProcessMemory
PROCESS_ALL_ACCESS = 0x1F0FFF


def find_process(process_name):
    def callback(hwnd, result):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(process_id)
            if process.name() == process_name:
                result.append((process_id, hwnd))
        return True

    process_ids = []
    win32gui.EnumWindows(callback, process_ids)
    if len(process_ids) != 1:
        raise AssertionError(f"{process_name} not found")

    return process_ids[0][0], process_ids[0][1]


pid, hWnd = find_process('Tibia.exe')   # I assume you have this from somewhere.
address = 0x0063FE68  # Likewise; for illustration I'll get the .exe header.

ADDRESS2 = ctypes.create_string_buffer(b"",4)
python_bytes_array = ctypes.string_at(ADDRESS2)
pi = ctypes.pointer(ADDRESS2)
bufferSize = len(ADDRESS2)
bytesRead = c_size_t()

processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)

number = 10000*100
WriteProcessMemory(processHandle, address, addressof(c_long(number)), sizeof(c_long), byref(bytesRead))
imgGrabber = ImageGrabber('Tibia')

img = imgGrabber.getImage()

#cropped_example = img.crop((1835, 322, 1835+31, 322+9))
#cropped_example.show()

for i in range(30000):
    number = i*100
    WriteProcessMemory(processHandle, address, addressof(c_long(number)), sizeof(c_long), byref(bytesRead))
    
    img = imgGrabber.getImage()
    #img = img.crop((322, 1835, 9, 31)).save('Test.bmp')
    if i % 100 == 0 :
        print(i)
    img = img.crop((1835, 322, 1835+31, 322+9)).save('dataset/{0}.bmp'.format(i))
    sleep(0.025)

CloseHandle(processHandle)


