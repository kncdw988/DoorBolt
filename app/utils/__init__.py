# coding:utf-8
import sys
import re
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QMouseEvent
from app.utils.const import Position
from pathlib import Path
from platform import platform
from typing import Union

from PyQt5.QtCore import QDir, QFileInfo, QProcess, QUrl, QOperatingSystemVersion
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtSql import QSqlDatabase


if sys.platform == "win32":
    from app.utils.win32 import WindowsMoveResize as MoveResize
else:
    raise RuntimeError("Unsupported system environment")


def startSystemMove(window: QWidget, globalPos: QPoint):
    """ resize window

    Parameters
    ----------
    window: QWidget
        window

    globalPos: QPoint
        the global point of mouse release event
    """
    MoveResize.startSystemMove(window, globalPos)


def starSystemResize(cls, window, globalPos, edges):
    """ resize window

    Parameters
    ----------
    window: QWidget
        window

    globalPos: QPoint
        the global point of mouse release event

    edges: `Qt.Edges`
        window edges
    """
    MoveResize.starSystemResize(window, globalPos, edges)


class Singleton:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)

        return cls._instance


def getPressedPos(widget: QWidget, e: QMouseEvent):
    """ Detect the position of the mouse down

    Parameters
    ----------
    widget: QWidget
        the widget which happens mouse press event

    e: QMouseEvent
        mouse press event

    Returns
    -------
    pressedPos: Position or None
        the position of the mouse click
    """
    pos = None
    w, h = widget.width(), widget.height()
    lx = 0 <= e.x() <= w // 3
    mx = w // 3 < e.x() <= w * 2 // 3
    rx = w * 2 // 3 < e.x() <= w
    ty = 0 <= e.y() <= h // 3
    my = h // 3 < e.y() <= h * 2 // 3
    by = h * 2 // 3 < e.y() <= h

    if lx and ty:
        pos = Position.TOP_LEFT
    elif mx and ty:
        pos = Position.TOP
    elif rx and ty:
        pos = Position.TOP_RIGHT
    elif lx and my:
        pos = Position.LEFT
    elif mx and my:
        pos = Position.CENTER
    elif rx and my:
        pos = Position.RIGHT
    elif lx and by:
        pos = Position.BOTTOM_LEFT
    elif mx and by:
        pos = Position.BOTTOM
    elif rx and by:
        pos = Position.BOTTOM_RIGHT

    return pos


def adjustName(name: str):
    """ adjust file name

    Returns
    -------
    name: str
        file name after adjusting
    """
    name = re.sub(r'[\\/:*?"<>|\r\n]+', "_", name).strip()
    return name.rstrip(".")


def getWindowsVersion():
    if "Windows-7" in platform():
        return 7

    build = sys.getwindowsversion().build
    version = 10 if build < 22000 else 11
    return version


def isGreaterEqualWin10():
    """ determine if the os version ≥ Win10 """
    return QOperatingSystemVersion.current() >= QOperatingSystemVersion.Windows10


def showInFolder(path: Union[str, Path]):
    """ show file in file explorer """
    if isinstance(path, Path):
        path = str(path.absolute())

    if not path or path.lower() == 'http':
        return

    if path.startswith('http'):
        QDesktopServices.openUrl(QUrl(path))
        return

    info = QFileInfo(path)   # type:QFileInfo
    if sys.platform == "win32":
        args = [QDir.toNativeSeparators(path)]
        if not info.isDir():
            args.insert(0, '/select,')

        QProcess.startDetached('explorer', args)
    elif sys.platform == "darwin":
        args = [
            "-e", 'tell application "Finder"', "-e", "activate",
            "-e", f'select POSIX file "{path}"', "-e", "end tell",
            "-e", "return"
        ]
        QProcess.execute("/usr/bin/osascript", args)
    else:
        url = QUrl.fromLocalFile(path if info.isDir() else info.path())
        QDesktopServices.openUrl(url)
