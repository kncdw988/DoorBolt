from PyQt5.QtWidgets import QWidget
from app.effect.win32 import WindowsEffect
from ctypes import cast
from ctypes.wintypes import LPRECT, MSG
from win32 import win32gui
from win32.lib import win32con
from PyQt5.QtGui import QCursor, QCloseEvent
from PyQt5.QtWidgets import QWidget, QApplication
from app.effect.const import LPNCCALCSIZE_PARAMS
from app.utils import win32 as win_utils
from PyQt5.QtWinExtras import QtWin


class FramelessWindow(QWidget):
    """Frameless window"""

    BORDER_WIDTH = 5

    def __init__(self, parent=None):
        super().__init__(parent)
        self.windowEffect = WindowsEffect()
        self._isResizeEnabled = True

        # add DWM shadow and window animation
        self.windowEffect.addWindowAnimation(self.winId())
        # self.windowEffect.addShadowEffect(self.winId())

        # handle multi screen with different dpi
        self.windowHandle().screenChanged.connect(self.__onScreenChanged)

        self.resize(500, 500)

    def setResizeEnabled(self, isEnabled: bool):
        """set whether resizing is enabled"""
        self._isResizeEnabled = isEnabled

    def nativeEvent(self, eventType, message):
        """handle the Windows message"""
        msg = MSG.from_address(message.__int__())
        if msg.message == win32con.WM_NCHITTEST and self._isResizeEnabled:
            pos = QCursor.pos()
            xPos = pos.x() - self.x()
            yPos = pos.y() - self.y()
            w, h = self.width(), self.height()
            lx = xPos < self.BORDER_WIDTH
            rx = xPos > w - self.BORDER_WIDTH
            ty = yPos < self.BORDER_WIDTH
            by = yPos > h - self.BORDER_WIDTH
            if lx and ty:
                return True, win32con.HTTOPLEFT
            elif rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif rx and ty:
                return True, win32con.HTTOPRIGHT
            elif lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            if msg.wParam:
                rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
            else:
                rect = cast(msg.lParam, LPRECT).contents

            isMax = win_utils.isMaximized(msg.hWnd)
            isFull = win_utils.isFullScreen(msg.hWnd)

            # adjust the size of client rect
            if isMax and not isFull:
                thickness = win_utils.getResizeBorderThickness(msg.hWnd)
                rect.top += thickness
                rect.left += thickness
                rect.right -= thickness
                rect.bottom -= thickness

            # handle the situation that an auto-hide taskbar is enabled
            if (isMax or isFull) and win_utils.Taskbar.isAutoHide():
                position = win_utils.Taskbar.getPosition(msg.hWnd)
                if position == win_utils.Taskbar.LEFT:
                    rect.top += win_utils.Taskbar.AUTO_HIDE_THICKNESS
                elif position == win_utils.Taskbar.BOTTOM:
                    rect.bottom -= win_utils.Taskbar.AUTO_HIDE_THICKNESS
                elif position == win_utils.Taskbar.LEFT:
                    rect.left += win_utils.Taskbar.AUTO_HIDE_THICKNESS
                elif position == win_utils.Taskbar.RIGHT:
                    rect.right -= win_utils.Taskbar.AUTO_HIDE_THICKNESS

            result = 0 if not msg.wParam else win32con.WVR_REDRAW
            return True, result

        return QWidget.nativeEvent(self, eventType, message)

    def __onScreenChanged(self):
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(
            hWnd,
            None,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED,
        )


class AcrylicWindow(FramelessWindow):
    """ A frameless window with acrylic effect """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__closeByKey = False

        QtWin.enableBlurBehindWindow(self)

        self.windowEffect.addWindowAnimation(self.winId())
        self.setStyleSheet("background:transparent")

    def nativeEvent(self, eventType, message):
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())
        if msg.message == win32con.WM_SYSKEYDOWN:
            if msg.wParam == win32con.VK_F4:
                self.__closeByKey = True
                QApplication.sendEvent(self, QCloseEvent())
                return False, 0

        return super().nativeEvent(eventType, message)

    def closeEvent(self, e):
        quitOnClose = QApplication.quitOnLastWindowClosed()
        if not self.__closeByKey or quitOnClose:
            self.__closeByKey = False
            return super().closeEvent(e)

        self.__closeByKey = False
        self.hide()
