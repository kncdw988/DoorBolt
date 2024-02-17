from app.view.base_window_win32 import AcrylicWindow
from PyQt5.QtWidgets import QAction, QApplication, QHBoxLayout, QWidget, qApp
from PyQt5.QtGui import (QDesktopServices, QDragEnterEvent, QDropEvent,
                         QIcon, QPixmap)
from PyQt5.QtCore import (QEasingCurve, QEvent, QEventLoop, QFile, QFileInfo,
                          Qt, QTimer, QUrl)
from app.components.widgets.stacked_widget import OpacityAniStackedWidget, PopUpAniStackedWidget
from app.components.widgets.label import PixmapLabel
from app.components.title_bar.title_bar import TitleBar
from app.components.thumbnail_tool_bar import ThumbnailToolBar


class SplashScreen(QWidget):
    """ Splash screen """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.logo = PixmapLabel(self)
        self.logo.setPixmap(QPixmap(":/images/logo/logo_splash_screen.png"))
        self.hBoxLayout.addWidget(self.logo, 0, Qt.AlignmentFlag.AlignCenter)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        color = '2b2b2b'
        self.setStyleSheet(f'background:#{color}')
    

class MainWindow(AcrylicWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isInSelectionMode = False
        self.navigationHistories = [("myMusicInterfaceStackWidget", 0)]
        self.setObjectName("mainWindow")
        self.createWidgets()
        self.initWidget()
        self.initHotkey()

    def initWindow(self):
        """ initialize window """
        r = self.devicePixelRatioF()
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        # self.resize(w*1240/1920, h*970/1080)
        # self.setMinimumSize(w*r*1030/1920, h*r*780/1080)

        self.setWindowTitle(self.tr("Groove Music"))
        # self.setWindowIcon(QIcon(":/images/logo/logo.ico"))

        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def createWidgets(self):
        """ create widgets """
        # main window contains totalStackWidget, playBar and titleBar
        # totalStackWidget contanins subMainWindow, playingInterface and videoWindow
        self.totalStackWidget = OpacityAniStackedWidget(self)

        # subMainWindow is used to put navigation interface and subStackWidget
        self.subMainWindow = QWidget(self)

        # create splash screen
        self.splashScreen = SplashScreen(self)

        # create title bar
        self.titleBar = TitleBar(self)

        # display the window on the desktop first
        self.initWindow()

        # subStackWidget contains myMusicInterface, albumInterface and other interface
        # that need to be displayed on the right side of navigationInterface
        self.subStackWidget = PopUpAniStackedWidget(self.subMainWindow)

        # # create setting interface
        # self.settingInterface = SettingInterface(self.subMainWindow)

        # create timer to update the position of lyrics
        self.updateLyricPosTimer = QTimer(self)

        # crete thumbnail bar
        self.thumbnailToolBar = ThumbnailToolBar(self)
        self.thumbnailToolBar.setWindow(self.windowHandle())


        # create navigation interface
        self.navigationInterface = NavigationInterface(self.subMainWindow)

        # create label navigation interface
        self.labelNavigationInterface = LabelNavigationInterface(
            self.subMainWindow)

        # create smallest play interface
        self.smallestPlayInterface = SmallestPlayInterface(
            self.mediaPlaylist.playlist, parent=self)

        # create system tray icon
        self.systemTrayIcon = SystemTrayIcon(self)

        # create search result interface
        self.searchResultInterface = SearchResultInterface(
            self.library, self.subMainWindow)

        # create more search result interface
        self.moreSearchResultInterface = MoreSearchResultInterface(
            self.library, self.subMainWindow)

        # create state tooltip
        self.scanInfoTooltip = None

        self.songTabSongListWidget = self.myMusicInterface.songListWidget

    def initLibrary(self):
        """ initialize library """
        pass