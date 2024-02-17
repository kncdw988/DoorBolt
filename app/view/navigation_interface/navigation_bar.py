# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout

from .navigation_button import CreatePlaylistButton, ToolButton, NIF
from .navigation_widget_base import NavigationWidgetBase


class NavigationBar(NavigationWidgetBase):
    """ Navigation bar """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__createButtons()
        self.vBox = QVBoxLayout()
        self.__initWidget()

    def __createButtons(self):
        """create buttons """
        self.showMenuButton = ToolButton(
            NIF.path(NIF.GLOBAL_NAVIGATION), iconSize=(26, 26), parent=self)
        self.searchButton = ToolButton(
            NIF.path(NIF.SEARCH), (60, 62), (24, 24), parent=self)
        self.myMusicButton = ToolButton(NIF.path(
            NIF.MUSIC_IN_COLLECTION), (60, 62), parent=self)
        self.historyButton = ToolButton(
            NIF.path(NIF.RECENT), (60, 62), parent=self)
        self.playingButton = ToolButton(
            NIF.path(NIF.PLAYING), (60, 62), parent=self)
        self.playlistButton = ToolButton(
            NIF.path(NIF.PLAYLIST), iconSize=(22, 22), parent=self)
        self.createPlaylistButton = CreatePlaylistButton(self)
        self.settingButton = ToolButton(NIF.path(NIF.SETTINGS), parent=self)

        # selected button
        self.currentButton = self.myMusicButton

        self.buttons = [
            self.showMenuButton, self.searchButton, self.myMusicButton,
            self.historyButton, self.playingButton, self.playlistButton,
            self.createPlaylistButton, self.settingButton
        ]

        self._selectableButtons = self.buttons[2:6] + [self.settingButton]

        self._selectableButtonNames = [
            'myMusicButton', 'historyButton', 'playingButton',
            'playlistButton', 'settingButton'
        ]

    def __initWidget(self):
        """ initialize widgets """
        self.setFixedWidth(60)
        self.setSelectedButton(self.myMusicButton.property('name'))
        self._connectButtonClickedSigToSlot()
        self.__initLayout()

    def __initLayout(self):
        """ initialize layout """
        self.vBox.addSpacing(40)
        self.vBox.setSpacing(0)
        self.vBox.setContentsMargins(0, 0, 0, 0)
        for button in self.buttons[:-1]:
            self.vBox.addWidget(button)

        self.vBox.addWidget(self.settingButton, 0, Qt.AlignmentFlag.AlignBottom)
        self.vBox.addSpacing(127)
        self.setLayout(self.vBox)
