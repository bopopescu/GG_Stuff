from PySide.QtGui import *
from PySide.QtCore import *
import os
import sys


class Panel(QWidget):
    def __init__(self):
        super(Panel, self).__init__()
        self.initUI()

        self.nukescripts = []
        self.dirname = ''
        self.basename = ''


    def initUI(self):
        self.menubar = QMenuBar()
        self.menubar.addMenu("&File")

        self.currentLabel = QLabel()
        self.currentLabel.setWordWrap(True)

        self.epilabel = QLabel("Episode")

        self.searchLine = QLineEdit("")
        self.searchLine.setMaxLength(3)

        self.listWidget = QListWidget()
        self.listWidget.setEditTriggers(False)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget.setAlternatingRowColors(True)

        self.renderBtn = QPushButton()
        self.renderBtn.setText("Render In Background")
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
        self.layout.addWidget(self.renderBtn)
        self.layout.addWidget(self.renderPNG)
        self.layout.addWidget(self.renderMov)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.hLayout)
        self.mainLayout.addLayout(self.layout)

        self.renderBtn.clicked.connect(self.renderSelectedNukescripts)
        self.renderPNG.clicked.connect(self.renderSequenceNukescripts)
        self.renderMov.clicked.connect(self.renderDNXHRNukescripts)
        self.searchLine.textChanged.connect(self.getNukescripts)
        self.listWidget.itemSelectionChanged.connect(self.selectedList)

        self.setWindowTitle("Nuke Manager")
        self.setFixedSize(400,500)

        self.setLayout(self.mainLayout)

    def renderSelectedNukescripts(self):
        currents = self.listWidget.selectedItems()
        # W:\Production\3D_Shots\106\Composite
        path = "W:\\Production\\3D_Shots\\" + self.searchLine.text() + "\\Composite"
        for current in currents:
            fullpath = os.path.join(path, str(current.text())).replace("/", "\\")
            os.system('A:\\Launchers\\Chameleon\\CML_Nuke_8_Terminal.bat {0}'.format(fullpath))
			
    def renderSequenceNukescripts(self):
        currents = self.listWidget.selectedItems()
        path = "W:\\Production\\3D_Shots\\" + self.searchLine.text() + "\\Composite"
        for current in currents:
            fullpath = os.path.join(path, str(current.text())).replace("/", "\\")
            os.system('A:\\Launchers\\Chameleon\\CML_Nuke_8_Terminal_PNG.bat {0}'.format(fullpath))		

    def renderDNXHRNukescripts(self):
        currents = self.listWidget.selectedItems()
        path = "W:\\Production\\3D_Shots\\" + self.searchLine.text() + "\\Composite"
        for current in currents:
            fullpath = os.path.join(path, str(current.text())).replace("/", "\\")
            os.system('A:\\Launchers\\Chameleon\\CML_Nuke_8_Terminal_DNXHR.bat {0}'.format(fullpath))	
            
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

def main():
    app = QApplication(sys.argv)
    panel = Panel()
    panel.show()
    sys.exit(app.exec_())\

if __name__ == '__main__':
    main()