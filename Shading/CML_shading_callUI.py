from maya import cmds, mel

from PyQt4 import uic
from shutil import copyfile
import getpass
import maya.OpenMaya as om
import PyQt4.QtCore as qc
import PyQt4.QtGui  as qg
import maya.OpenMayaUI as omui
import os, sys, sip, pymel.core, maya, getpass, ConfigParser, linecache
sys.path.append("A:/Ticklers/Chameleon/Shading")
import CML_shading_command as sc
reload(sc)

#global userName
userName = getpass.getuser()
#global prefsPath
prefsPath = ("C:/Users/%s/Desktop/KAZOOPS/Preferences/" %userName)
#global notesPath
notesPath =  ("C:/Users/%s/Desktop/KAZOOPS/Notes/" %userName)
#global projectDir	
projectDir	   = "Q:/Production/3D_Shots/"
if cmds.file(q = True, exists = True) :
	#global maya_files
	maya_files = cmds.file(query = True, sceneName = True)
	#global maya_shots
	maya_shots 	= cmds.file(query = True, sceneName = True, shortName = True).split(".ma")[0]
	#global maya_episode
	maya_episode = maya_files.split("/")[3]

# function to get main Maya window
def get_maya_main_window( ):
    ptr = maya.OpenMayaUI.MQtUtil.mainWindow( )
    main_win = sip.wrapinstance( long( ptr ), qc.QObject )
    return main_win
    
# Path to the designer UI file
UI_fileName = "A:/Ticklers/Chameleon/Shading/CML_shading_UI.ui"
objs_class, base_class = uic.loadUiType(UI_fileName)
form_class, base_class = uic.loadUiType(UI_fileName)

#Interface Class
class EZ_Tools_UI(base_class, form_class, objs_class):
	def __init__(self, parent = get_maya_main_window(), *args ):
		super( base_class, self ).__init__( parent )
		self.setupUi(self)
		self.setObjectName('UI_fileName')

#-----------------------------------------------------------------------------------------------------------------#
	# EZ_Shading
#-----------------------------------------------------------------------------------------------------------------#	
		#self.get_shotsName()
		
		self.pushButton_open_001.clicked.connect(self.open_mayaFile)
		self.pushButton_open_002.clicked.connect(self.open_referenceFile)		
		self.pushButton_stepOne.clicked.connect(self.activateButton_001)
		self.pushButton_stepTwo.clicked.connect(self.activateButton_002)
		self.pushButton_stepThree.clicked.connect(self.activateButton_003)
		#self.pushButton_execute.clicked.connect(self.allInOne)
		self.pushButton_stepFour.clicked.connect(sc.createCamera)
		self.pushButton_stepFive.clicked.connect(sc.createLight)
		self.horizontalSlider_Y_lightRotation.valueChanged.connect(self.slider_moved) 
		self.pushButton_stepSix.clicked.connect(sc.vraySky)
		self.pushButton_stepSeven.clicked.connect(sc.addSubdiv)
		self.pushButton_saveSHD_file.clicked.connect(sc.saveMayaSHDFile)
		self.pushButton_ImageSaveFile.clicked.connect(sc.saveImageFile)
		self.pushButton_cleanFile.clicked.connect(sc.cleanFile)

    	  		
	def dock_ui( self ):
		if pymel.core.dockControl( 'myToolDock', q = 1, ex = 1 ):
			pymel.core.deleteUI( 'myToolDock' )
		floatingLayout = pymel.core.paneLayout( configuration = 'single', width = 300, height = 400 )
		pymel.core.dockControl( 'myToolDock', area = 'right',  content = floatingLayout, label = 'EZ Tool' )
		pymel.core.control( 'UI_fileName', e = True, p = floatingLayout )
		return True
	
#-----------------------------------------------------------------------------------------------------------------#
	# EZ_Shading
#-----------------------------------------------------------------------------------------------------------------#	
	
	"""def get_shotsName(self):
		self.comboBox_shotsName_list.clear()
		types = self.comboBox_types_list.itemText(self.comboBox_types_list.currentIndex())
		shots = os.listdir("W:/Production/CML_Assets/")
		self.comboBox_shotsName_list.addItems(shots)"""
	
	def open_mayaFile(self):
		types = self.comboBox_types_list.itemText(self.comboBox_types_list.currentIndex())
		multipleFilters = "Maya Files (*.ma *.mb)"
		"""fileName = cmds.fileDialog2(fileFilter = multipleFilters, dialogStyle=2, caption = 'Open', dir = 
		"W:/Production/CML_Assets/%s/%s"%(types, shots), fileMode = 1)
		cmds.file( fileName[0], f=True, options='v=1', o = True  )"""
		fileFolder= "W:/Production/CML_Assets/%s/"%(types)
		fileOpen = cmds.fileDialog2(dialogStyle=2, caption = 'Open', dir = (fileFolder) , fileMode = 1)
		print fileOpen[0]
		#os.startfile(fileOpen[0])
		cmds.file(new = True, force = True)
		cmds.file(fileOpen[0], open = True)
	
	def open_referenceFile(self):
		episodes = cmds.file(query=True,sceneName=True).split('/')[5]
		types = cmds.file(query=True,sceneName=True).split('/')[4]
		folders = os.listdir("Q:/Preproduction/Designs")
		for folder in folders:
			if folder.startswith('KAZ01_%s'%(episodes)):
				referenceFolder = "W:/Preproduction/Designs/%s/%s"%(types, folder)
				referenceFile = cmds.fileDialog2(dialogStyle=2, caption = 'Open', dir = (referenceFolder) , fileMode = 1)
				print referenceFille
				#os.startfile(referenceFile[0])
	
	def activateButton_001(self):
		self.pushButton_stepOne.clicked.connect(self.activateButton_001)
		sc.switch2Vray()

			
	def activateButton_002(self):
		self.pushButton_stepTwo.clicked.connect(self.activateButton_002)
		sc.LoadKAZPresets()
	
	def activateButton_003(self):
		self.pushButton_stepThree.clicked.connect(self.activateButton_003)
		sc.changeTextureAttribute()

	
	def allInOne(self):
		self.pushButton_execute.clicked.connect(self.activateButton_001)
		self.pushButton_execute.clicked.connect(self.activateButton_002)
		self.pushButton_execute.clicked.connect(self.activateButton_003)
	
	def slider_moved(self, position):
		self.label_lightRotationNumber.setText('%d' %position)
		cmds.setAttr("LIGHTRIG.rotateY", -position)

    	 		
#-----------------------------------------------------------------------------------------------------------------#  		
def createWindows():
	global dialog
	try:
		dialog.close()
	except:
		pass
	dialog = EZ_Tools_UI()
	dialog.show()
createWindows()
def create():
    EZ_Tools_UI().dock_ui()