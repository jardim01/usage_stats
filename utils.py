from enum import Enum
import ctypes
import win32process
import psutil
import json
import win32gui
import win32con
import ctypes
import os
from win32gui import GetForegroundWindow, GetWindowText


def get_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def save_json(path, data):
    data_copy = data.copy()
    tmp_path = f'{path}.tmp'
    with open(tmp_path, 'w') as f:
        json.dump(data_copy, f)
    # Avoid data corruption (os.rename is atomic)
    os.replace(tmp_path, path)


def get_foreground_exe():
    window = GetForegroundWindow()
    pid = win32process.GetWindowThreadProcessId(window)[-1]
    try:
        return psutil.Process(pid=pid).exe()
    except psutil.NoSuchProcess as e:
        print(e)
    except ValueError as e:
        print(e)

    return None


def is_locked():
    fw = ctypes.windll.User32.GetForegroundWindow()
    if fw == 0:
        return True
    if GetWindowText(fw) == "Windows Default Lock Screen":
        return True

    return False


def is_idle():
    if is_locked():
        return True
    if win32gui.SystemParametersInfo(win32con.SPI_GETSCREENSAVERRUNNING):
        return True

    return False


def is_active():
    return not is_idle()


class Style(Enum):
    OK = 0
    OKCANCEL = 1
    ABORTRETRYIGNORE = 2
    YESNOCANCEL = 3
    YESNO = 4
    RETRYCANCEL = 5
    CANCELTRYAGAINCONTINUE = 6


class Icon(Enum):
    NONE = 0x0
    STOP = 0x10
    ERROR = 0x10
    HAND = 0x10
    QUESTION = 0x20
    EXCLAMATION = 0x30
    WARNING = 0x30
    INFORMATION = 0x40
    ASTERISK = 0x40


def show_message_box(
    title: str,
    text: str,
    style: Style = Style.OK,
    icon: Icon = Icon.NONE
):
    return ctypes.windll.user32.MessageBoxW(
        0,
        text,
        title,
        style.value | icon.value
    )
