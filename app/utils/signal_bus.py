# coding:utf-8
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtMultimedia import QMediaPlaylist

from app.utils import Singleton


class SignalBus(Singleton, QObject):
    """ Signal bus """
    appMessageSig = pyqtSignal(object)          # APP 发来消息
    appErrorSig = pyqtSignal(str)               # APP 发生异常
    appRestartSig = pyqtSignal()                # APP 需要重启



    showMainWindowSig = pyqtSignal()      # 显示主界面
    fullScreenChanged = pyqtSignal(bool)  # 全屏/退出全屏


signalBus = SignalBus()
