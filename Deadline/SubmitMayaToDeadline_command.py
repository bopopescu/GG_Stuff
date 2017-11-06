from maya import cmds, mel
from PyQt4 import uic
import maya.OpenMayaUI as omui
import xml.etree.ElementTree as et
import PyQt4.QtCore as qc
import PyQt4.QtGui	as qg
import sip, sys, getpass, os
import Deadline.SubmitMayaToDeadline_function
import subprocess

if cmds.file(q = True, exists = True) :
	pass
else:
	sys.exit("No Maya File is Open")

# function to get main Maya window
def get_maya_main_window( ):
	ptr = omui.MQtUtil.mainWindow( )
	main_win = sip.wrapinstance( long( ptr ), qc.QObject )
	return main_win

# path to the designer UI file
UI_fileName = "A:/Ticklers/Chameleon/Deadline/SubmitMayaToDeadline_UI.ui"
objs_class, base_class = uic.loadUiType(UI_fileName)
form_class, base_class = uic.loadUiType(UI_fileName)

### define
maya_files = cmds.file(sceneName=True, query = True )
fileName = maya_files.split("/")[-1].rpartition(".")[0]
episodeCode = fileName.split("_")[1]
projectPath	   = maya_files.split(episodeCode)[0] + episodeCode
outputPath	 = ("Z:/CML_Output/Production/3D_Shots/" + episodeCode + "/Output/Render/")
jobScriptFolder = "X:/custom/scripts/JobScript/"
userName = getpass.getuser()
deadlineDataPath = ("C:/Users/%s/Desktop/Chameleon/Deadline/Data/")%(userName)
deadlineDataFullPath = deadlineDataPath + "DatadeadlineData.xml"
deadline = Deadline.SubmitMayaToDeadline_function.Deadline()


if cmds.getAttr("defaultRenderGlobals.currentRenderer") == "vray":
	resWidth = cmds.getAttr("vraySettings.width")
	resHeight = cmds.getAttr("vraySettings.height")
	imageFormat = cmds.getAttr("vraySettings.imageFormatStr")
	fileNamePadding = cmds.getAttr("vraySettings.fileNamePadding")
	padding = "#" * fileNamePadding
elif cmds.getAttr("defaultRenderGlobals.currentRenderer") == "mayaSoftware" or cmds.getAttr("defaultRenderGlobals.currentRenderer") == "mentalRay":
	resWidth = cmds.getAttr("defaultResolution.width")
	resHeight = cmds.getAttr("defaultResolution.height")
	

### setLayer frame range
if cmds.objExists("SetLayer"):
	cmds.editRenderLayerGlobals(currentRenderLayer = "SetLayer")
	min_frame_SetLayer = int(cmds.getAttr('defaultRenderGlobals.startFrame'))
	max_frame_SetLayer = int(cmds.getAttr('defaultRenderGlobals.endFrame'))
	frame_SetLayer = str(min_frame_SetLayer) +("-") + str(max_frame_SetLayer)
	cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")

### deadline data
if not os.path.exists(deadlineDataPath):
	from shutil import copyfile
	os.makedirs(deadlineDataPath)
	copyfile("A:/Ticklers/Chameleon/Deadline/data/deadlineData.xml", deadlineDataFullPath)
tree = et.parse(deadlineDataFullPath)
root = tree.getroot()

#Interface Class
class SubmitMayaToDeadline(base_class, form_class, objs_class):
	def __init__(self, parent = get_maya_main_window(), *args ):
		super( base_class, self ).__init__( parent )
		self.setupUi(self)
		self.setObjectName('UI_fileName')

#-----------------------------------------------------------------------------------------------------------------#
	# Submit_2_Deadline
#-----------------------------------------------------------------------------------------------------------------#
		self.get_jobSettings()
		self.get_jobName()
		self.horizontalSlider_priority.valueChanged.connect(self.slider_moved_prio)
		self.horizontalSlider_framesPerTask.valueChanged.connect(self.slider_moved_framesPerTask)
		self.horizontalSlider_threads.valueChanged.connect(self.slider_moved_threads)
		self.getProjectPath()
		self.getOutputPath()
		self.checkBox_overrideLayerJobSettings.clicked.connect(self.enabledFrameList)
		#self.checkBox_multipleSender.clicked.connect(self.multipleSender)
		self.pushButton_submitJob.clicked.connect(self.submit2Deadline)
		self.lineEdit_preJobScript.setText("X:/custom/scripts/JobScript/PreJobScript.py")
		self.lineEdit_postJobScript.setText("X:/custom/scripts/JobScript/PostJobScript.py")
		self.toolButton_preJobScript.clicked.connect(self.preJobScript)
		#self.toolButton_postJobScript.clicked.connect(self.postJobScript)

#-----------------------------------------------------------------------------------------------------------------#
	def dock_ui( self ):
		if pymel.core.dockControl( 'myToolDock', q = 1, ex = 1 ):
			pymel.core.deleteUI( 'myToolDock' )
		floatingLayout = pymel.core.paneLayout( configuration = 'single', width = 300, height = 400 )
		pymel.core.dockControl( 'myToolDock', area = 'right',  content = floatingLayout, label = 'Submit to Deadline' )
		pymel.core.control( 'UI_fileName', e = True, p = floatingLayout )
		return True


#-----------------------------------------------------------------------------------------------------------------#
	# Submit_2_Deadline
#-----------------------------------------------------------------------------------------------------------------#

	def get_jobSettings(self):
		for settings in root.findall('settings'):
			#dept = settings.find('dept').text
			prio = settings.find('prio').text
			fpt = settings.find('fpt').text
			threads = settings.find('threads').text
			
		#self.lineEdit_department.setText(dept)
		#self.comboBox_group.setText(grp)
		self.horizontalSlider_priority.setValue(int(prio))
		self.lineEdit_priority.setText(str(prio))
		self.horizontalSlider_framesPerTask.setValue(int(fpt))
		self.lineEdit_framesPerTask.setText(str(fpt))
		self.horizontalSlider_threads.setValue(int(threads))
		self.lineEdit_threads.setText(str(threads))

	def get_jobName(self):
		maya_shots	= cmds.file(query = True, sceneName = True, shortName = True).split(".ma")[0]
		self.lineEdit_jobName.setText(maya_shots)

	def slider_moved_prio(self, prio):
		self.lineEdit_priority.setText('%d' %prio)
		prio = self.horizontalSlider_priority.value()
		self.lineEdit_priority.setText(str(prio))

	def slider_moved_framesPerTask(self, fpt):
		self.lineEdit_framesPerTask.setText('%d' %fpt)
		fpt = self.horizontalSlider_framesPerTask.value()
		self.lineEdit_framesPerTask.setText(str(fpt))

	def slider_moved_threads(self, threads):
		self.lineEdit_threads.setText('%d' %threads)
		threads = self.horizontalSlider_threads.value()
		self.lineEdit_threads.setText(str(threads))

	def getProjectPath(self):
		self.lineEdit_projectPath.setText(projectPath)

	def getOutputPath(self):
		outputPath = cmds.workspace(fileRuleEntry = "images")
		self.lineEdit_outputPath.setText(outputPath)

	def preJobScript(self):
		jobScript = cmds.fileDialog2(dialogStyle=1, dir = (jobScriptFolder) , fileMode = 1)
		self.lineEdit_preJobScript.setText(jobScript[0])
		
	def postJobScript(self):
		jobScript = cmds.fileDialog2(dialogStyle=1, dir = (jobScriptFolder) , fileMode = 1)
		self.lineEdit_postJobScript.setText(jobScript[0])
		
	def enabledFrameList(self):
		if self.checkBox_overrideLayerJobSettings.isChecked():
			self.lineEdit_frameList.setEnabled(True)
		else:
			self.lineEdit_frameList.setEnabled(False)
	
	def multipleSender(self):
		if self.checkBox_multipleSender.isChecked() == True:
			self.setMinimumWidth(1080)
			self.setMaximumWidth(1080)
			self.setFixedWidth(1080)
		else:
			self.setMinimumWidth(540)
			self.setMaximumWidth(540)
			self.setFixedWidth(540)
	
	def whatsThis(self):
		pass
						
#-----------------------------------------------------------------------------------------------------------------#
	def submit2Deadline(self):
		def disableSetLayer():
			if not cmds.objExists("SetLayer") or cmds.objExists("SetLayer_PREPASS"):
				cmds.setAttr("SetLayer_PREPASS.renderable", 0)
				cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")

			elif cmds.objExists("SetLayer"):
				cmds.setAttr("SetLayer.renderable", 0)
				cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")

		dept = self.lineEdit_department.text()
		grp = self.comboBox_group.currentText()
		pool = self.comboBox_pool.currentText()
		s_pool = self.comboBox_secondaryPool.currentText()
		prio = self.lineEdit_priority.text()
		fpt = self.lineEdit_framesPerTask.text()
		threads = self.lineEdit_threads.text()
		initialStatus = self.checkBox_submitAsSuspended.isChecked()
		preJS = self.lineEdit_preJobScript.text()
		postJS = self.lineEdit_postJobScript.text()
		
		
		if initialStatus == True:
			initialStatus = "Suspended"
		else:
			initialStatus = "Active"

		root[0][0].text = str(dept)
		root[0][1].text = str(grp)
		root[0][2].text = str(pool)
		root[0][3].text = str(s_pool)
		root[0][4].text = str(prio)
		root[0][5].text = str(fpt)
		root[0][6].text = str(threads)
		root[0][7].text = str(initialStatus)
		QSpecifiedFrame = self.checkBox_overrideLayerJobSettings.isChecked()
		if QSpecifiedFrame == True:
			specifiedFrame = self.lineEdit_frameList.text()
			root[0][8].text = str(specifiedFrame)
		else:
			pass
		tree.write(deadlineDataFullPath)

		### get all renderLayer
		renderLayerON = [x for x in cmds.ls(type = "renderLayer") if (cmds.getAttr(x+".renderable") == 1)]
		renderLayerReference = [y for y in cmds.ls(type = "renderLayer") if (cmds.referenceQuery(y, inr = True))]
		try:
			renderLayerON.remove("SetLayer")
		except:
			pass
		for rlr in renderLayerReference:
			try:
				renderLayerON.remove(rlr)
			except:
				pass
		
		for i in range(len(renderLayerON)):
			cmds.editRenderLayerGlobals(currentRenderLayer = renderLayerON[i])
			### frame range
			min_frame = int(cmds.getAttr('defaultRenderGlobals.startFrame'))
			max_frame = int(cmds.getAttr('defaultRenderGlobals.endFrame'))
			deadline.BatchName						= fileName
			deadline.ChunkSize						= fpt
			if renderLayerON[i]=="Matte" or renderLayerON[i]=="Shadow":
				deadline.ConcurrentTasks								= 3
				deadline.TaskTimeoutMinutes				= 30
			elif renderLayerON[i]=="AO":
				deadline.ConcurrentTasks								= 3
				deadline.TaskTimeoutMinutes				= 90
			else:
				deadline.ConcurrentTasks								= 1
				deadline.TaskTimeoutMinutes				= 90
			deadline.Department						= dept
			deadline.Group							= grp
			exactFrame = str(min_frame)+("-")+str(max_frame)
			QSpecifiedFrame = self.checkBox_overrideLayerJobSettings.isChecked()
			if QSpecifiedFrame == True:
				deadline.Frames							=  specifiedFrame
				deadline.PreJobScript					= preJS
				deadline.PostJobScript					= postJS
			else:
				deadline.Frames							=  exactFrame
				deadline.PreJobScript					= preJS
				deadline.PostJobScript					= postJS
			deadline.InitialStatus						= initialStatus
			deadline.JobDependencies				= ""
			deadline.Name								= fileName + ' - ' + renderLayerON[i]
			deadline.OutputDirectory0				= outputPath + "%s/%s" % (fileName,	 renderLayerON[i])
			deadline.OutputFilename0				= renderLayerON[i] + ".%s.%s" % (padding, imageFormat)
			deadline.OutputFilePath					= outputPath
			deadline.OutputFilePrefix				= "%s/<Layer>/<Layer>" % (fileName)
			deadline.Pool								= pool
			deadline.SecondaryPool					= s_pool
			deadline.Priority								= prio
			deadline.ProjectPath						= projectPath
			deadline.RenderLayer						= renderLayerON[i]
			deadline.SceneFile							= maya_files
			deadline.UserName							= userName
			deadline.Version							= 2014
			deadline.ImageHeight					= resHeight
			deadline.ImageWidth						= resWidth

			maya_job									= deadline.build_maya_job_info()
			maya_plugin									=  deadline.build_maya_plugin_info() 

			if os.path.isfile(maya_files):
				deadline.submit_to_deadline(maya_job, maya_plugin)

			try:
				if not cmds.objExists("SetLayer") and cmds.getAttr("SetLayer.renderable") == 1:
					cmds.confirmDialog(message='Files Submitted       ')
			except:
				pass

		if cmds.objExists("SetLayer") and cmds.getAttr("SetLayer.renderable") == 1:
			### get setlayer_prepass jobids
			get_jobs = subprocess.Popen(['C:/Program Files/Thinkbox/Deadline7/bin/deadlinecommand.exe', 'GetJobIdsFilter', 'JobName=%s - SetLayer_PREPASS'%fileName],
			stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
			jobs = get_jobs.communicate()
			job = jobs[0]
			deadline.BatchName						= fileName
			deadline.ChunkSize						= fpt
			deadline.ConcurrentTasks				= 1
			deadline.Department						= dept
			deadline.Group							= grp
			if QSpecifiedFrame == True:
				deadline.Frames							=  specifiedFrame
				deadline.PostJobScript					= ""
			else:
				deadline.Frames							=  frame_SetLayer
				deadline.PreJobScript					= preJS
				deadline.PostJobScript					= postJS
			deadline.InitialStatus						= initialStatus
			deadline.JobDependencies				= job
			deadline.Name								= fileName + ' - ' + "SetLayer"
			deadline.OutputDirectory0				= outputPath + "%s/%s" % (fileName,	 "SetLayer")
			deadline.OutputFilename0				= "SetLayer.%s.%s" % (padding, imageFormat)
			deadline.OutputFilePath					= outputPath
			deadline.OutputFilePrefix				= "%s/<Layer>/<Layer>" % (fileName)
			deadline.Pool								= pool
			deadline.SecondaryPool					= s_pool
			deadline.Priority								= prio
			deadline.ProjectPath						= projectPath
			deadline.RenderLayer						= "SetLayer"
			deadline.SceneFile							= maya_files
			deadline.TaskTimeoutMinutes				= 90
			deadline.UserName							= userName
			deadline.Version							= 2014
			deadline.ImageHeight					= resHeight
			deadline.ImageWidth						= resWidth

			maya_job									= deadline.build_maya_job_info()
			maya_plugin								= deadline.build_maya_plugin_info()

			if os.path.isfile(maya_files):
				deadline.submit_to_deadline(maya_job, maya_plugin)
			disableSetLayer()
			cmds.confirmDialog(message='Files Submitted       ')

#-----------------------------------------------------------------------------------------------------------------#
def createWindows():
	global dialog
	try:
		dialog.close()
	except:
		pass
	dialog = SubmitMayaToDeadline()
	dialog.show()

def create():
	SubmitMayaToDeadline().dock_ui()

createWindows()