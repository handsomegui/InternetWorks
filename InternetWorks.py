#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Gui (pekingmaster@gmail.com)


import sys
from subprocess import call
from time import sleep

from PyQt4.QtGui import *
from PyQt4.QtCore import QThread, SIGNAL

import icons


cmd_str, opt1, opt2, opt3 = 'ping', '-q', '-o', '-t 1'
check_target = ['www.apple.com']    # Add targets as you want.


class SysTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(SysTrayIcon, self).__init__(parent)

        self.okIcon = QIcon(':/ok.png')
        self.failIcon = QIcon(':/broken.png')

        self.initUI()

        self.checkThread = CheckThread()
        self.checkThread.start()

        self.connect(self.checkThread, SIGNAL('inet'), self.statusToggle)

    def initUI(self):
        if self.isSystemTrayAvailable():
            self.setIcon(self.okIcon)

            self.quitAction = QAction('Quit', self)

            self.trayMenu = QMenu()
            self.trayMenu.addAction(self.quitAction)
            self.connect(self.quitAction, SIGNAL('triggered()'), self.quitAll)

            self.setContextMenu(self.trayMenu)
            self.setVisible(True)

    def statusToggle(self, status):
        if status == 'OK':
            self.setIcon(self.okIcon)
        elif status == 'FAILED':
            self.setIcon(self.failIcon)

    def quitAll(self):
        self.checkThread.quit()
        self.hide()
        del self
        sys.exit(0)


class CheckThread(QThread):
    def ping_it(self, domain_name):
        ping_cmd = "%s %s %s %s %s" % (cmd_str, opt1, opt2, opt3, domain_name)
        ret = call(ping_cmd, shell=True)
        if ret == 0:    # Ping successfully.
            results_list.append(1)

    def run(self):
        global results_list
        results_list = []

        while 1:
            sleep(1.5)

            # Trigger the checking.
            map(self.ping_it, check_target)

            if results_list:
                self.emit(SIGNAL('inet'), 'OK')
            else:
                self.emit(SIGNAL('inet'), 'FAILED')

            # Clear the list.
            results_list = []


if __name__ == '__main__':
    app = QApplication([])
    tray = SysTrayIcon(app)
    tray.show()
    sys.exit(app.exec_())
