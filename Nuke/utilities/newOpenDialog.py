from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtGui import QTableWidgetItem
from PySide.QtUiTools import *

import sys
import os
import nuke
import nukescripts

from datetime import time
from datetime import date
from datetime import datetime

class NukePanel(QWidget):
    def __init__(self):
        super(NukePanel, self).__init__()
        self.initUI()

    def initUI(self):

        # *********************************************************************************

        self.sLabel = QLabel()
        self.sLabel.setText("Episode")

        self.sLine = QLineEdit()
        # self.sLine.setText('101')
        self.sLine.setMaxLength(3)

        self.sBtn = QPushButton()
        self.sBtn.setText('Search')

        self.hLayout1 = QHBoxLayout()
        self.hLayout1.addWidget(self.sLabel)
        self.hLayout1.addWidget(self.sLine)

        # *********************************************************************************

        # *********************************************************************************

        self.cItems = QLabel()
        self.cItems.setText("Data :")
        self.sItems = QLabel()
        self.sItems.setText("Item Selected : 0")

        # *********************************************************************************

        # *********************************************************************************

        self.hHeader = ['Nukescripts', 'Date Modified']

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.countRow()))
        # self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnCount(len(self.hHeader))
        self.tableWidget.setHorizontalHeaderLabels(self.hHeader)
        self.getData()
        self.tableWidget.setColumnWidth(0, 175)
        self.tableWidget.setColumnWidth(1, 175)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.sortItems(0, Qt.AscendingOrder)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        self.vLayout2 = QVBoxLayout()
        self.vLayout2.addWidget(self.cItems)
        self.vLayout2.addWidget(self.sItems)
        self.vLayout2.addWidget(self.tableWidget)

        # *********************************************************************************

        # *********************************************************************************

        self.openBtn = QPushButton()
        self.openBtn.setText("Open Selected Items")

        self.vLayout1 = QVBoxLayout()
        self.vLayout1.addWidget(self.openBtn)

        # *********************************************************************************

        # *********************************************************************************

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.hLayout1)
        self.mainLayout.addLayout(self.vLayout2)
        self.mainLayout.addLayout(self.vLayout1)

        self.setLayout(self.mainLayout)

        self.setFixedSize(700, 800)

        # *********************************************************************************

        # *********************************************************************************

        self.sLine.textChanged.connect(self.getData)
        self.tableWidget.itemSelectionChanged.connect(self.getSelectedItems)
        self.openBtn.clicked.connect(self.openSelectedNukescripts)

        # *********************************************************************************

        # *********************************************************************************
    
    def getPath(self, episode):
        return "W:\\Production\\3D_Shots\\"+episode+"\\Composite"

    def countRow(self):
        if len(self.sLine.text()) == 3:
            nukePath = self.getPath(self.sLine.text())
            count = [x for x in os.listdir(nukePath) if x.endswith(".nk")]
            self.cItems.setText("Data : "+ str(len(count)))
        elif len(self.sLine.text()) < 3:
            count = ''
            self.cItems.setText("Data : " + str(len(count)))
        return count

    def getNukescripts(self):
        if len(self.sLine.text()) == 3:
            nukePath = self.getPath(self.sLine.text())
            count = [x for x in os.listdir(nukePath) if x.endswith(".nk")]
            count.sort()
            timeList = []
            for c in count:
                fullPath = os.path.join(nukePath, c).replace('\\', '/')
                timestamps = datetime.fromtimestamp(os.path.getmtime(fullPath))
                cTimestamps = str(timestamps)
                concatList = c, cTimestamps
                timeList.append(concatList)
            for m,n in enumerate(timeList):
                self.tableWidget.insertRow(m)
                self.tableWidget.setItem(m, 0, QTableWidgetItem(n[0]))
                self.tableWidget.setItem(m, 1, QTableWidgetItem(n[1]))
        else:
            self.tableWidget.setRowCount(0)

    def getSelectedItems(self):
        if len(self.sLine.text()) == 3:
            currents = []
            for current in self.tableWidget.selectedItems():
                currents.append(current.text().encode('ascii'))
                currents.sort()
            self.sItems.setText("Item Selected : {0}".format(str(currents)))
        else:
            self.sItems.setText("Item Selected : 0")

    def getData(self):
        self.countRow()
        self.getNukescripts()

        # *********************************************************************************

        # *********************************************************************************


    def openSelectedNukescripts(self):
        currents = self.tableWidget.selectedItems()
        currents.sort()
        path = self.getPath(self.sLine.text())
        for current in currents:
            print current.text()
            fullpath = os.path.join(path, str(current.text())).replace("/", "\\")
            nuke.scriptOpen(fullpath)


def main():
    main.panel = NukePanel()
    main.panel.show()