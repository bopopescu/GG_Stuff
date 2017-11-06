from PySide.QtGui import *
from PySide.QtCore import *
import os
import getpass
import sys
import nuke
import nukescripts


class NukePanel(QWidget):
    def __init__(self):
        super(NukePanel, self).__init__()
        self.initUI()

    def initUI(self):
        self.user = getpass.getuser()
        # self.first = str.capitalize(self.user.split('.')[0])
        # self.last = str.capitalize(self.user.split('.')[1])

        self.epilabel = QLabel("Search")

        self.searchLine = QLineEdit("")
        self.searchLine.setMaxLength(3)

        self.listWidget = QListWidget()
        #self.listWidget.setEditTriggers(False)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setAlternatingRowColors(True)

        self.openSelectedBtn = QPushButton()
        self.openSelectedBtn.setText("Open Selected Nukescripts")
        
        self.changeWrite =QPushButton()
        self.changeWrite.setText('Change Write Node into Proper DNXHR')

        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.epilabel)
        self.hLayout.addWidget(self.searchLine)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.openSelectedBtn)
        self.layout.addWidget(self.changeWrite)

        self.masterLayout = QVBoxLayout()
        self.masterLayout.addLayout(self.hLayout)
        self.masterLayout.addLayout(self.layout)

        self.openSelectedBtn.clicked.connect(self.openSelectedNukescripts)
        self.searchLine.textChanged.connect(self.getNukescripts)
        self.changeWrite.clicked.connect(self.changeWriteNode)
        
        self.openSelectedBtn.setShortcut(QKeySequence('Enter'))

        # self.setWindowTitle("Nuke Manager --- %s %s" % (self.first, self.last))
        self.setFixedSize(400, 500)

        self.setLayout(self.masterLayout)
        
    def writeNode(self):
        old = nuke.toNode('WriteMov_DNXHR')
        oldx = old.xpos()
        oldy = old.ypos()
        oldin = old.input(0)
        nuke.delete(old)
        nuke.scriptReadFile("W:\Production\Comp_Library\Comp_Tools\CMLWrite_DNXHR.nk")
        new = nuke.toNode('WriteMov_DNXHR')
        new.setXpos(oldx)
        new.setYpos(oldy)
        new.setInput(0, oldin)
        
    def addWriteConnectToTimecode(self):
        timecode = nuke.toNode('AddTimeCode1')
        if timecode:
            timex = timecode.xpos()
            timey = timecode.ypos()
            nuke.scriptReadFile("W:\Production\Comp_Library\Comp_Tools\CMLWrite_DNXHR.nk")
            new = nuke.toNode('WriteMov_DNXHR')
            new.setXpos(timex+100)
            new.setYpos(timey)
            new.setInput(0, timecode)
        else:
            wNode = nuke.toNode('WriteMov')
            wNodex = wNode.xpos()
            wNodey = wNode.ypos()
            wNodeIn = wNode.input(0)

            tNode = nuke.createNode('AddTimeCode')
            tNode.setXpos(wNodex)
            tNode.setYpos(wNodey-100)
            tNode.setInput(0,wNodeIn)
            
            tNodes = nuke.toNode('AddTimeCode1')
            tNodex = tNodes.xpos()
            tNodey = tNodes.ypos()
            nuke.scriptReadFile("W:\Production\Comp_Library\Comp_Tools\CMLWrite_DNXHR.nk")
            new = nuke.toNode('WriteMov_DNXHR')
            new.setXpos(tNodex+100)
            new.setYpos(tNodey)
            new.setInput(0, tNodes)
            
    def checkNodeCMLpath(self):
        if nuke.toNode('CMLPath'):
            print "CMLPath Node Already Exists"
        else:
            nuke.scriptReadFile("W:\Production\Comp_Library\Comp_Tools\CMLPath.nk")
        
    def checkNukescriptName(self):
        nullName = nuke.root()['name'].value()
        if not nullName == "":
            basename = os.path.basename(nullName)
            name, ext = os.path.splitext(basename)
            episode = name.split('_')[1]
            act = name.split('_')[2].split('-')[0]
            shot =  name.split('_')[2].split('-')[1]
            return episode, act, shot
            
    def inputNametoPath(self):
        episode = self.checkNukescriptName()[0]
        act = self.checkNukescriptName()[1]
        shot = self.checkNukescriptName()[2]
        
        cmlPath = nuke.toNode('CMLPath')
        cmlPath['Episode'].setValue(episode)
        cmlPath['Act'].setValue(act)
        cmlPath['Scene'].setValue(shot)
        
    def checkWriteNodeDNXHR(self):
        if nuke.toNode('WriteMov_DNXHR'):
            print "WriteMov_DNXHR Node Already Exists"
        else:
            nuke.scriptReadFile("W:\Production\Comp_Library\Comp_Tools\CMLWrite_DNXHR.nk")
            
    def checkTimeCode(self):
        if nuke.toNode('AddTimeCode1'):
            print "AddTimeCode1 Node Already Exists"
        else:
            nuke.createNode('AddTimeCode')
            
    def setupAdditionalNode(self):
        wMovNode = nuke.toNode('WriteMov')
        wdMovNode = nuke.toNode('WriteMov_DNXHR')
        timecodeNode = nuke.toNode('AddTimeCode1')
        
        wMovNodeInput = wMovNode.input(0)
        wMovNodeX = wMovNode.xpos()
        wMovNodeY = wMovNode.ypos()
        
        timecodeNode.setXpos(wMovNodeX)
        timecodeNode.setYpos(wMovNodeY-25)
        timecodeNode.setInput(0, wMovNodeInput)
        
        tNodeX = timecodeNode.xpos()
        tNodeY = timecodeNode.ypos()
        
        wdMovNode.setXpos(tNodeX+150)
        wdMovNode.setYpos(tNodeY-12)
        wdMovNode.setInput(0,timecodeNode)
        wMovNode.setInput(0,timecodeNode)
        
    def executeSetup(self):
        self.checkNodeCMLpath()
        self.checkNukescriptName()
        self.inputNametoPath()
        self.checkWriteNodeDNXHR()
        self.checkTimeCode()
        self.setupAdditionalNode()
        
    def changeName(self):
        nodeMov = nuke.toNode('WriteMov1')
        if nodeMov:
            nodeMov['name'].setValue('WriteMov')
            print 'Node Name Has been Changed'
        

    def openSelectedNukescripts(self):
        currents = self.listWidget.selectedItems()
        currents.sort()
        path = "W:\\Production\\3D_Shots\\" + self.searchLine.text() + "\\Composite"
        for current in currents:
            print current.text()
            fullpath = os.path.join(path, str(current.text())).replace("/", "\\")
            nuke.scriptOpen(fullpath)
            
    def changeWriteNode(self):
        currents = self.listWidget.selectedItems()
        currents.sort()
        path = "W:\\Production\\3D_Shots\\" + self.searchLine.text() + "\\Composite"
        for current in currents:
            print current.text()
            fullpath = os.path.join(path, str(current.text())).replace("/", "\\")
            nuke.scriptClear()
            nuke.scriptOpen(fullpath)
            self.executeSetup()
            nuke.scriptSave()
        
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

def main():
    main.panel = NukePanel()
    main.panel.show()
