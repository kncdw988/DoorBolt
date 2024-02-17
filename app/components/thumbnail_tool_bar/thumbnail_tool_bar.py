# coding:utf-8
from app.utils.config import Theme
from app.utils.signal_bus import SignalBus
from components.widgets.menu import MIF
from PyQt5.QtGui import QIcon
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton



class WindowsThumbnailToolBar(QWinThumbnailToolBar):
    """ Thumbail tool bar """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.playButton = ThumbnailPlayButton(self)
        self.lastSongButton = QWinThumbnailToolButton(self)
        self.nextSongButton = QWinThumbnailToolButton(self)
        self.__initWidget()

    def __initWidget(self):
        """ initialize widgets """
        self.lastSongButton.setIcon(QIcon(":/images/thumbnail_tool_bar/Previous.svg"))
        self.nextSongButton.setIcon(QIcon(":/images/thumbnail_tool_bar/Next.svg"))

        # add button to bar
        self.addButton(self.lastSongButton)
        self.addButton(self.playButton)
        self.addButton(self.nextSongButton)


    def setButtonsEnabled(self, isEnable: bool):
        """ set button enabled """
        for button in self.buttons():
            button.setEnabled(isEnable)

    def setPlay(self, isPlay: bool):
        """ set play state """
        self.playButton.setPlay(isPlay)


class ThumbnailPlayButton(QWinThumbnailToolButton):
    """ Thumbnail play button"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setPlay(False)

    def setPlay(self, isPlay: bool):
        """ set play state """
        self.isPlaying = isPlay
        if self.isPlaying:
            self.setIcon(QIcon(":/images/thumbnail_tool_bar/Pause.svg"))
        else:
            self.setIcon(QIcon(":/images/thumbnail_tool_bar/Play.svg"))
