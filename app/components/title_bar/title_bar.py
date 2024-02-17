# coding:utf-8
import sys

from app.utils.style_sheet import setStyleSheet
from app.utils import startSystemMove
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QLabel, QWidget

from app.components.title_bar.title_bar_buttons import MaximizeButton, TitleBarButton


class TitleBar(QWidget):
    """ Title bar """

    def __new__(cls, *args, **kwargs):
        cls = WindowsTitleBar
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, parent):
        super().__init__(parent)
        self.resize(600, 40)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.titleLabel = QLabel(self.tr("Groove Music"), self)
        self.minButton = TitleBarButton(parent=self)
        self.closeButton = TitleBarButton(parent=self)
        self.returnButton = TitleBarButton((60, 40), self)
        self.maxButton = MaximizeButton(self)
        self.__initWidget()

    def __initWidget(self):
        """ initialize widgets """
        self.setFixedHeight(40)
        self.__setQss()

        self.titleLabel.hide()
        self.returnButton.hide()

        # connect signal to slot
        self.minButton.clicked.connect(self.window().showMinimized)
        self.maxButton.clicked.connect(self.__showRestoreWindow)
        self.closeButton.clicked.connect(self.window().close)

        self.returnButton.installEventFilter(self)
        self.titleLabel.installEventFilter(self)
        self.window().installEventFilter(self)

    def __setQss(self):
        """ set style sheet """
        self.titleLabel.setObjectName("titleLabel")
        self.minButton.setObjectName("minButton")
        self.maxButton.setObjectName("maxButton")
        self.closeButton.setObjectName("closeButton")
        self.returnButton.setObjectName("returnButton")
        setStyleSheet(self, 'title_bar')

    def resizeEvent(self, e: QResizeEvent):
        self.titleLabel.move(self.returnButton.isVisible() * 60, 0)
        self.closeButton.move(self.width() - 57, 0)
        self.maxButton.move(self.width() - 2 * 57, 0)
        self.minButton.move(self.width() - 3 * 57, 0)

    def mouseDoubleClickEvent(self, e):
        self.__showRestoreWindow()

    def __showRestoreWindow(self):
        """ show restored window """
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def setWhiteIcon(self, isWhiteIcon: bool):
        """ set icon color """
        for button in self.findChildren(TitleBarButton):
            button.setWhiteIcon(isWhiteIcon)

    def eventFilter(self, obj, e: QEvent):
        if obj is self.returnButton:
            if e.type() == QEvent.Type.Hide:
                self.titleLabel.move(0, 0)
            elif e.type() == QEvent.Type.Show:
                self.titleLabel.move(60, 0)
        elif obj is self.titleLabel:
            if e.type() == QEvent.Type.Show:
                self.titleLabel.move(60*self.returnButton.isVisible(), 0)
        elif obj is self.window():
            if e.type() == QEvent.Type.WindowStateChange:
                self.maxButton.setMaxState(self.window().isMaximized())
                self.maxButton.setAttribute(Qt.WidgetAttribute.WA_UnderMouse, False)
                return False
        elif obj is self.window():
            if e.type() == QEvent.Type.WindowStateChange:
                self.maxButton.setMaxState(self.window().isMaximized())
                return False

        return super().eventFilter(obj, e)

    def _isDragRegion(self, pos):
        """ Check whether the pressed point belongs to the area where dragging is allowed """
        for button in self.findChildren(TitleBarButton):
            if button.isVisible() and button.isPressed:
                return False

        left = self.returnButton.isVisible() * 60
        right = self.width() - 46 - 92 * self.minButton.isVisible()
        return left < pos.x() < right


class WindowsTitleBar(TitleBar):
    """ Title bar for Windows system """

    def mouseMoveEvent(self, event):
        if not self._isDragRegion(event.pos()):
            return

        startSystemMove(self.window(), event.globalPos())


class LinuxTitleBar(TitleBar):
    """ Title bar for Linux system """

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton or not self._isDragRegion(event.pos()):
            return

        startSystemMove(self.window(), event.globalPos())
