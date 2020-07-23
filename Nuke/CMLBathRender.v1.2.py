from PySide.QtGui import *
from PySide.QtCore import *
import os
import sys
import time


class Panel(QWidget):
    def __init__(self):
        super(Panel, self).__init__()
        self.initUI()

        self.nukescripts = []
        self.dirname = ''
        self.basename = ''

    def initUI(self):
        self.currentLabel = QLabel()
        self.currentLabel.setWordWrap(True)

        self.epilabel = QLabel("Episode")

        self.searchLine = QLineEdit("")
        self.searchLine.setMaxLength(3)

        self.listWidget = QListWidget()
        self.listWidget.setEditTriggers(False)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget.setAlternatingRowColors(True)

        self.renderPNG = QPushButton()
        self.renderPNG.setText("Render PNG Seq")
        self.renderMov = QPushButton()
        self.renderMov.setText("Render Mov DNXHR")

        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.epilabel)
        self.hLayout.addWidget(self.searchLine)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.currentLabel)
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.renderPNG)
        self.layout.addWidget(self.renderMov)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.hLayout)
        self.mainLayout.addLayout(self.layout)

        self.renderPNG.clicked.connect(self.renderSequenceNukescripts)
        self.renderMov.clicked.connect(self.renderDNXHRNukescripts)
        self.searchLine.textChanged.connect(self.getNukescripts)
        self.listWidget.itemSelectionChanged.connect(self.selectedList)

        self.setWindowTitle("Nuke Manager v1.2")
        self.setFixedSize(400, 500)

        self.setLayout(self.mainLayout)

    def renderSequenceNukescripts(self):
        currents = self.listWidget.selectedItems()
        path = "W:\\Production\\3D_Shots\\" + self.searchLine.text() + "\\Composite"
        for current in currents:
            fullpath = os.path.join(path, str(current.text())).replace("/", "\\")
            os.system('A:\\Launchers\\Chameleon\\CML_Nuke_8_Terminal_PNG.bat {0}'.format(fullpath))

    def renderDNXHRNukescripts(self):
        currents = self.listWidget.selectedItems()
        path = "W:\\Production\\3D_Shots\\" + self.searchLine.text() + "\\Composite"
        self.renderThread = RenderThread(currents, path)
        self.renderThread.start()

    def getNukescripts(self):
        newfile = []
        if len(self.searchLine.text()) == 3:
            path = "W:\\Production\\3D_Shots\\" + self.searchLine.text() + "\\Composite"
            files = os.listdir(path)
            for file in files:
                if file.endswith('.nk'):
                    newfile.append(file)
                    newfile.sort()
            self.listWidget.addItems(newfile)
        if len(self.searchLine.text()) < 3:
            self.listWidget.clear()

    def selectedList(self):
        currents = []
        for current in self.listWidget.selectedItems():
            currents.append(current.text().encode('ascii'))
            currents.sort()
        self.currentLabel.setText("Current Selection : {0}".format(str(currents)))

class RenderThread(QThread):
    def __init__(self, currents, path):
        super(RenderThread, self).__init__()
        self.currents = currents
        self.path = path

    def __del__(self):
        self.wait()

    def run(self):
        for current in self.currents:
            try:
                current.setForeground(QBrush(Qt.green, Qt.SolidPattern))
                fullpath = os.path.join(self.path, str(current.text())).replace("/", "\\")
                os.system('A:\\Launchers\\Chameleon\\CML_Nuke_8_Terminal_DNXHR.bat {0}'.format(fullpath))
            except Exception as e:
                current.setForeground(QBrush(Qt.red, Qt.SolidPattern))
                print(e)
            finally:
                current.setForeground(QBrush(Qt.gray, Qt.SolidPattern))


def main():
    app = QApplication(sys.argv)
    panel = Panel()
    panel.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
