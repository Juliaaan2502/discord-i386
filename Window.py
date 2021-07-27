from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import sys
import os
import time


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Discord Web")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'Discord-Logo.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Version 1.0.0 Testing"))
        layout.addWidget(QLabel("By Juliaaan2502"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setGeometry(0, 0, 1525, 884)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Zurück", self)
        back_btn.setStatusTip("Zurück zur vorherigen Seite")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "Vorwärts", self)
        next_btn.setStatusTip("Weiter")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), "Seite neuladen", self)
        reload_btn.setStatusTip("Discord neuladen")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "Discord Startseite", self)
        home_btn.setStatusTip("zur Discord-Startseite")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        file_menu = self.menuBar().addMenu("&Neu")

        new_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "Neuer Discord-App Tab", self)
        new_tab_action.setStatusTip("Öffne einen neuen Discord-App Tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        help_menu = self.menuBar().addMenu("&Hilfe")

        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "Über Discord-Web Potierung", self)
        about_action.setStatusTip("Finde mehr über diese Potierung von Discord heraus!")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_discord_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')),
                                            "Discord Startseite", self)
        navigate_discord_action.setStatusTip("Gehe zu discord.com!")
        navigate_discord_action.triggered.connect(self.navigate_discord)
        help_menu.addAction(navigate_discord_action)

        exit_action = QAction(QIcon(os.path.join('images', 'cross-circle.png')),
                                            "Discord beenden", self)
        exit_action.setStatusTip("Beenden von Discord Web")
        exit_action.triggered.connect(self.close)
        help_menu.addAction(exit_action)

        self.add_new_tab(QUrl('http://discord.com'), 'Homepage')

        self.show()

        self.setWindowTitle("Discord Web")
        self.setWindowIcon(QIcon(os.path.join('images', 'Discord-Logo.png')))

    def close(self, argv1):
        time.sleep(1)
        exit()

    def add_new_tab(self, qurl=None, label="Neuer Tab"):

        if qurl is None:
            qurl = QUrl('https://discord.com/app')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()

        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Discord Web" % title)

    def navigate_discord(self):
        self.tabs.currentWidget().setUrl(QUrl("https://discord.com"))

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://discord.com"))


app = QApplication(sys.argv)
app.setApplicationName("Discord Web")
app.setOrganizationName("Discord Inc.")
app.setOrganizationDomain("discord.com")

window = MainWindow()

app.exec_()
