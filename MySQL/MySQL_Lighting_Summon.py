import xml.etree.ElementTree as et
import PyQt4.QtCore as qc
import PyQt4.QtGui	as qg
import sys, getpass, os,subprocess, base64
from PyQt4 import uic
sys.path.append("A:/Ticklers/Chameleon/MySQL")
import DB_manager
from MySQL.FrameLayout import FrameLayout
from MySQL.SmartsheetData import SmartsheetData
from PyQt4 import uic
from datetime import datetime
from functools import partial 
### define
userName = getpass.getuser()
giggleManager_path = ("C:/Users/%s/Desktop/Chameleon/GiggleManager/")%(userName)
giggleManager_fullPath = giggleManager_path + "GiggleManager.xml"

### history 
if not os.path.exists(giggleManager_path):
	from shutil import copyfile
	os.makedirs(giggleManager_path)
	copyfile("A:/Ticklers/Chameleon/MySQL/GiggleManager.xml", giggleManager_fullPath)
tree = et.parse(giggleManager_fullPath)
root = tree.getroot()
        
### path to the designer UI file
myDatabase_expanded_UI = "A:/Ticklers/Chameleon/MySQL/Database_Expanded_UI.ui"
objsClass_md_expanded, baseClass_md_expanded = uic.loadUiType(myDatabase_expanded_UI)

myDatabase_UI = "A:/Ticklers/Chameleon/MySQL/Database_UI.ui"
objsClass_md, baseClass_md = uic.loadUiType(myDatabase_UI)

class CustomComboBox(qg.QComboBox):
	def wheelEvent(self, event):
		event.ignore()
		
class UpdateTable(object):
	def updateHeaderItem(self, checkBox = None, horizontalHeaderLabel = None, headerFilter = None):
		horizontalHeaderCount = 0

		if checkBox.isChecked():
			horizontalHeaderCount = horizontalHeaderCount + 1
			for hf in root.iter(headerFilter):
				hf.text = str("True")
			return horizontalHeaderCount, horizontalHeaderLabel
		else:
			for hf in root.iter(headerFilter):
				hf.text = str("False")
			return horizontalHeaderCount, None

				
	def updateCheckBox(self, headerFilter = None, checkBox = None): 
		for hf in root.findall('headerFilter'):
			try:
				if hf.find(headerFilter).text == "True":
				    checkBox.setChecked(True)
			except:
				pass

		
class MyDatabase_R_Expanded(baseClass_md_expanded, objsClass_md_expanded, qg.QWidget):
	value = []
	def __init__(self, parent = None):
		super(MyDatabase_R_Expanded, self).__init__(parent)
		self.setupUi(self)
		self.setObjectName('myDatabase_R_expanded_UI')
		
		self.pushButton_login.clicked.connect(self.godMode)
		self.horizontalSlider_rowNumber.valueChanged.connect(self.set_lineEdit_rowNumber) 
		self.lineEdit_rowNumber_001.returnPressed.connect(self.set_horizontalSlider_rowNumber) 
		self.pushButton_setRow.clicked.connect(self.getRow_001)
		self.pushButton_addRow.clicked.connect(self.getRow_002)
		self.pushButton_addColumn.clicked.connect(self.getColumn)
		
	def godMode(self):
		if self.lineEdit_id.text() == base64.b64decode("Y29sZW9uMTk5Mg==") and \
		self.lineEdit_password.text() == base64.b64decode("Y29sZW9uOTIwMTI3MDM1NTYx"):
			self.groupBox_godMode.setEnabled(True)

	def set_lineEdit_rowNumber(self, value):
		self.lineEdit_rowNumber_001.setText('%d' %value)
		
	def set_horizontalSlider_rowNumber(self):
		value = self.lineEdit_rowNumber_001.text()
		self.horizontalSlider_rowNumber.setValue(int(value))

	def getRow_001(self):
		del self.value[:]
		row = self.lineEdit_rowNumber_001.text()
		self.value.append(int(row))

	def getRow_002(self):
		del self.value[:]
		if self.radioButton_before.isChecked():
			self.value.append(int(self.lineEdit_rowNumber_002.text())-1)
		if self.radioButton_after.isChecked():
			self.value.append(int(self.lineEdit_rowNumber_002.text()))

	def getColumn(self):
		del self.value[:]
		self.value.append(str(self.lineEdit_insertColumnName.text()))
				 						         				
class MyDatabase(baseClass_md, objsClass_md, qg.QWidget):
	def __init__(self, schema, table, tableLH, parent = None):
		super( MyDatabase, self ).__init__(parent)
		self.DB = DB_manager.DatabaseUtility(schema, table)
		self.DB_history = DB_manager.DatabaseUtility(schema, tableLH)
		self.setupUi(self)
		self.setObjectName('myDatabase_UI')
		
#-----------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#                  
		verticalLayout = self.verticalLayout_L_expanded

		self.horizontalLayout_id = qg.QHBoxLayout()
		self.horizontalLayout_id_history = qg.QHBoxLayout()
		self.horizontalLayout_shot = qg.QHBoxLayout()
		self.horizontalLayout_date = qg.QHBoxLayout()
		self.horizontalLayout_time = qg.QHBoxLayout()
		self.horizontalLayout_artist = qg.QHBoxLayout()
		self.horizontalLayout_startFrame = qg.QHBoxLayout()		
		self.horizontalLayout_endFrame = qg.QHBoxLayout()		
		self.horizontalLayout_mastershot = qg.QHBoxLayout()
		self.horizontalLayout_status = qg.QHBoxLayout()

		self.toolButton_id = qg.QToolButton()
		self.toolButton_id_history = qg.QToolButton()
		self.toolButton_shot = qg.QToolButton()
		self.toolButton_date = qg.QToolButton()
		self.toolButton_time = qg.QToolButton()
		self.toolButton_artist = qg.QToolButton()
		self.toolButton_startFrame = qg.QToolButton()	
		self.toolButton_endFrame = qg.QToolButton()	
		self.toolButton_mastershot = qg.QToolButton()
		self.toolButton_status = qg.QToolButton()
		
		expanded_toolButton_list = [self.toolButton_id, self.toolButton_id_history, self.toolButton_shot,
		self.toolButton_date, self.toolButton_time, self.toolButton_artist, self.toolButton_startFrame,
		self.toolButton_endFrame, self.toolButton_mastershot, self.toolButton_status]
		for expanded_toolButton in expanded_toolButton_list:
			expanded_toolButton.setText("+")

		disabled_toolButton_list = [self.toolButton_id, self.toolButton_id_history, self.toolButton_shot,
		self.toolButton_date, self.toolButton_time, self.toolButton_artist, self.toolButton_startFrame, 
		self.toolButton_endFrame, self.toolButton_mastershot, self.toolButton_status]
		for disabled_toolButton in disabled_toolButton_list:
			disabled_toolButton.setEnabled(False)
				
		fl = FrameLayout(title="Filter Header")		
		verticalLayout.addWidget(fl)
		self.checkBox_id = qg.QCheckBox("ID")
		self.checkBox_id_history = qg.QCheckBox("ID_History")
		self.checkBox_shot = qg.QCheckBox("Shot")
		self.checkBox_date = qg.QCheckBox("Date")
		self.checkBox_time = qg.QCheckBox("Time")
		self.checkBox_startFrame = qg.QCheckBox("Start_Frame")
		self.checkBox_endFrame = qg.QCheckBox("End_Frame")
		self.checkBox_artist = qg.QCheckBox("Artist")
		self.checkBox_mastershot = qg.QCheckBox("Mastershot")
		self.checkBox_status = qg.QCheckBox("Status")

		self.horizontalLayout_id.addWidget(self.checkBox_id)
		self.horizontalLayout_id.addWidget(self.toolButton_id)
		self.horizontalLayout_id_history.addWidget(self.checkBox_id_history)
		self.horizontalLayout_id_history.addWidget(self.toolButton_id_history)
		self.horizontalLayout_shot.addWidget(self.checkBox_shot)
		self.horizontalLayout_shot.addWidget(self.toolButton_shot)
		self.horizontalLayout_date.addWidget(self.checkBox_date)
		self.horizontalLayout_date.addWidget(self.toolButton_date)
		self.horizontalLayout_time.addWidget(self.checkBox_time)
		self.horizontalLayout_time.addWidget(self.toolButton_time)											
		self.horizontalLayout_artist.addWidget(self.checkBox_artist)
		self.horizontalLayout_artist.addWidget(self.toolButton_artist)
		self.horizontalLayout_startFrame.addWidget(self.checkBox_startFrame)
		self.horizontalLayout_startFrame.addWidget(self.toolButton_startFrame)
		self.horizontalLayout_endFrame.addWidget(self.checkBox_endFrame)											
		self.horizontalLayout_endFrame.addWidget(self.toolButton_endFrame)		
		self.horizontalLayout_mastershot.addWidget(self.checkBox_mastershot)
		self.horizontalLayout_mastershot.addWidget(self.toolButton_mastershot)
		self.horizontalLayout_status.addWidget(self.checkBox_status)
		self.horizontalLayout_status.addWidget(self.toolButton_status)
		
		fl.addLayout(self.horizontalLayout_id)	
		fl.addLayout(self.horizontalLayout_id_history)		
		fl.addLayout(self.horizontalLayout_shot)	
		fl.addLayout(self.horizontalLayout_date)	
		fl.addLayout(self.horizontalLayout_time)	
		fl.addLayout(self.horizontalLayout_artist)	
		fl.addLayout(self.horizontalLayout_startFrame)	
		fl.addLayout(self.horizontalLayout_endFrame)	
		fl.addLayout(self.horizontalLayout_mastershot)
		fl.addLayout(self.horizontalLayout_status)

		self.listWidget_bodyFilter = qg.QListWidget()
		self.listWidget_bodyFilter.setSelectionMode(qg.QAbstractItemView.ExtendedSelection)
		fl.addWidget(self.listWidget_bodyFilter)
						
		self.pushButton_refliter = qg.QPushButton("Refilter")
		fl.addWidget(self.pushButton_refliter)

		verticalSpacer = qg.QSpacerItem(120, 100, qg.QSizePolicy.Minimum, qg.QSizePolicy.Expanding)
		verticalLayout.addItem(verticalSpacer)
#-----------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#    		
		self.updateCheckBox()
		self.updateTable()
		self.updateTable_history()
		self.tableWidget_data.itemClicked.connect(self.updateTable_history)
		self.pushButton_save.clicked.connect(self.saveTable)
		self.pushButton_refliter.clicked.connect(self.updateTable)
		self.toolButton_godMode.clicked.connect(self.myDatabaseExpanded)	
		self.checkBox_artist.toggled.connect(self.setEnabled_artist)
		self.checkBox_mastershot.toggled.connect(self.setEnabled_mastershot)
		self.checkBox_status.toggled.connect(self.setEnabled_status)
		self.toolButton_status.clicked.connect(self.statusFilter)
#-----------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#			
	def statusFilter(self):
		columns = self.DB.GetColumns()
		tables = self.DB.GetTable()
		status = []
		for col in range(len(columns)):
			if columns[col][0] == "Status":
				for row in tables:
					status.append(row[col])
		self.listWidget_bodyFilter.clear()
		self.listWidget_bodyFilter.addItems(["Status Filter"])
		self.listWidget_bodyFilter.addItems(list(set(status)))
		for item in range(self.listWidget_bodyFilter.count()):
			self.listWidget_bodyFilter.item(item).setTextAlignment(qc.Qt.AlignCenter)  
		self.listWidget_bodyFilter.item(0).setFlags(qc.Qt.ItemIsSelectable)
		

			
	def setEnabled_artist(self):
		if self.checkBox_artist.isChecked():
			self.toolButton_artist.setEnabled(True)
		else:
			self.toolButton_artist.setEnabled(False)

	def setEnabled_mastershot(self):
		if self.checkBox_mastershot.isChecked():
			self.toolButton_mastershot.setEnabled(True)
		else:
			self.toolButton_mastershot.setEnabled(False)

	def setEnabled_status(self):
		if self.checkBox_status.isChecked():
			self.toolButton_status.setEnabled(True)
		else:
			self.toolButton_status.setEnabled(False)
							
	def myDatabaseExpanded(self):
		myDatabase_expanded = MyDatabase_R_Expanded(self)
		myDatabase_expanded.pushButton_createSmartsheet.clicked.connect(self.createTable_by_smartsheetData)
		myDatabase_expanded.pushButton_setRow.clicked.connect(self.setRow)	
		myDatabase_expanded.pushButton_addRow.clicked.connect(self.addRow) 
		myDatabase_expanded.pushButton_addColumn.clicked.connect(self.addColumn)
		myDatabase_expanded.pushButton_removeColumn.clicked.connect(self.removeColumn)
		myDatabase_expanded.show()		
        
	def setRow(self):
		self.tableWidget_data.setRowCount(int(MyDatabase_R_Expanded().value[0]))
		del MyDatabase_R_Expanded().value[:]
			
	def addRow(self):
		self.tableWidget_data.insertRow(int(MyDatabase_R_Expanded().value[0]))
		del MyDatabase_R_Expanded().value[:]

	def addColumn(self):
		column = 0
		self.tableWidget_data.insertColumn(column)
		self.tableWidget_data.setHorizontalHeaderLabels([MyDatabase_R_Expanded().value[0]])
		del MyDatabase_R_Expanded().value[:]

	def removeColumn(self):
		column = 0
		self.tableWidget_data.removeColumn(column)	
									
	def contextMenuEvent(self, events):
		status_menus = qg.QMenu(self)
		artist_menus = qg.QMenu(self)
		
		self.SentForStill = qg.QAction('Sent for Still', self)
		self.ReadyToCheck = qg.QAction('Ready to Check', self)
		self.ToStart = qg.QAction('To Start', self)
		self.WIP = qg.QAction('WIP', self)
		self.Revise = qg.QAction('Revise', self)
		self.Approved = qg.QAction('Approved', self)
		self.OnHold = qg.QAction('On Hold', self)
		self.Retake = qg.QAction('Retake', self)
		self.SentToFarm = qg.QAction('Sent to Farm', self)
		self.ReadyForComp = qg.QAction('Ready for Comp', self)

		self.Loong = qg.QAction('Loong', self)
		
		self.SentForStill.triggered.connect(lambda: self.lightingStatus(events, 'Sent for Still'))
		self.ReadyToCheck.triggered.connect(lambda: self.lightingStatus(events, 'Ready to Check'))
		self.ToStart.triggered.connect(lambda: self.lightingStatus(events, 'To Start'))
		self.WIP.triggered.connect(lambda: self.lightingStatus(events, 'WIP'))
		self.Revise.triggered.connect(lambda: self.lightingStatus(events, 'Revise'))
		self.Approved.triggered.connect(lambda: self.lightingStatus(events, 'Approved'))
		self.OnHold.triggered.connect(lambda: self.lightingStatus(events, 'On Hold'))
		self.Retake.triggered.connect(lambda: self.lightingStatus(events, 'Retake'))
		self.SentToFarm.triggered.connect(lambda: self.lightingStatus(events, 'Sent to Farm'))
		self.ReadyForComp.triggered.connect(lambda: self.lightingStatus(events, 'Ready for Comp'))

		self.Loong.triggered.connect(lambda: self.lightingArtist(events, 'Loong'))
								
		rightClickActions = [self.SentForStill, self.ReadyToCheck, self.ToStart, self.WIP, self.Revise,
									  self.Approved, self.OnHold, self.Retake, self.SentToFarm, self.ReadyForComp]
									  
		for rightClickAction in rightClickActions:
			status_menus.addAction(rightClickAction)
			
		artist_menus.addAction(self.Loong)

		if self.tableWidget_data.currentColumn() == 1:
			artist_menus.popup(qg.QCursor.pos())
					
		if self.tableWidget_data.currentColumn() == 4:
			status_menus.popup(qg.QCursor.pos())

	def lightingStatus(self, events, status):
		selectedItem = self.tableWidget_data.selectedItems()
		columnCount = self.tableWidget_data.columnCount()
		for item in selectedItem:
			row = item.row()
			col = item.column()
			for column in range(columnCount):
				if self.tableWidget_data.horizontalHeaderItem(column).text() == "Status":
					self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(status)))    
					self.setStatusColor()			

	def lightingArtist(self, events, name):
		selectedItem = self.tableWidget_data.selectedItems()
		columnCount = self.tableWidget_data.columnCount()
		for item in selectedItem:
			row = item.row()
			col = item.column()
			for column in range(columnCount):
				if self.tableWidget_data.horizontalHeaderItem(column).text() == "Artist":
					self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(name)))    
					self.setArtistColor()		
						    		   
	def setStatusColor(self):
		rowCount = self.tableWidget_data.rowCount()
		columnCount = self.tableWidget_data.columnCount()
		for row in range(rowCount):
			for column in range(columnCount):
				if self.tableWidget_data.horizontalHeaderItem(column).text() == "Status":
					if self.tableWidget_data.item(row,column).text() == 'Sent for Still':
						self.tableWidget_data.item(row, column).setBackground(qg.QColor(180,220,255))
						self.tableWidget_data.item(row, column).setTextColor(qg.QColor(0,0,0))
					if self.tableWidget_data.item(row,column).text() == 'Ready to Check':
						self.tableWidget_data.item(row, column).setBackground(qg.QColor(85,255,200))
						self.tableWidget_data.item(row, column).setTextColor(qg.QColor(0,0,0))
					if self.tableWidget_data.item(row,column).text() == 'To Start':
						self.tableWidget_data.item(row, column).setBackground(qg.QColor(255,211,135))
						self.tableWidget_data.item(row, column).setTextColor(qg.QColor(0,0,0))
					if self.tableWidget_data.item(row,column).text() == 'WIP':
						self.tableWidget_data.item(row, column).setBackground(qg.QColor(205,200,85))
						self.tableWidget_data.item(row, column).setTextColor(qg.QColor(0,0,0))
					if self.tableWidget_data.item(row,column).text() == 'Revise':
						self.tableWidget_data.item(row, column).setBackground(qg.QColor(205,15,5))
						self.tableWidget_data.item(row, column).setTextColor(qg.QColor(0,0,0))
					if self.tableWidget_data.item(row,column).text() == 'Approved':
						self.tableWidget_data.item(row, column).setBackground(qg.QColor(255,130,220))
						self.tableWidget_data.item(row, column).setTextColor(qg.QColor(0,0,0))	
					if self.tableWidget_data.item(row,column).text() == 'On Hold':
						self.tableWidget_data.item(row, column).setBackground(qg.QColor(5,15,205))
						self.tableWidget_data.item(row, column).setTextColor(qg.QColor(0,0,0))
					if self.tableWidget_data.item(row,column).text() == 'Retake':
						self.tableWidget_data.item(row, column).setBackground(qg.QColor(110,25,20))
						self.tableWidget_data.item(row, column).setTextColor(qg.QColor(0,0,0))
					if self.tableWidget_data.item(row,column).text() == 'Sent to Farm':
						self.tableWidget_data.item(row, column).setBackground(qg.QColor(85,200,255))
						self.tableWidget_data.item(row, column).setTextColor(qg.QColor(0,0,0))
					if self.tableWidget_data.item(row,column).text() == 'Ready for Comp':
						self.tableWidget_data.item(row, column).setBackground(qg.QColor(20,185,25))
						self.tableWidget_data.item(row, column).setTextColor(qg.QColor(0,0,0))
					self.tableWidget_data.item(row, column).setTextAlignment(qc.Qt.AlignCenter)	

	def setArtistColor(self):
		rowCount = self.tableWidget_data.rowCount()
		columnCount = self.tableWidget_data.columnCount()
		for row in range(rowCount):
			for column in range(columnCount):
				if self.tableWidget_data.horizontalHeaderItem(column).text() == "Artist":
					if self.tableWidget_data.item(row,column).text() == 'Loong':
						self.tableWidget_data.item(row, column).setBackground(qg.QColor(180,220,255))
						self.tableWidget_data.item(row, column).setTextColor(qg.QColor(0,0,0))
					self.tableWidget_data.item(row, column).setTextAlignment(qc.Qt.AlignCenter)	
					
	def updateTable_history(self):
		columns = self.DB_history.GetColumns()
		tables = self.DB_history.GetTable()
		getRow = self.tableWidget_data.currentRow()
		displayed_columns = ["Shot", "Date", "Time", "Artist", "Start_Frame", "End_Frame"]
		for column in range(len(displayed_columns)):
				self.treeWidget_history.headerItem().setText(column, displayed_columns[column])
				self.treeWidget_history.headerItem().setTextAlignment(column, qc.Qt.AlignCenter)
		self.treeWidget_history.clear()
		for table in range(len(tables)):
			if tables[table][1]-1 == getRow:
				qg.QTreeWidgetItem(self.treeWidget_history)
				row = self.treeWidget_history.topLevelItemCount()-1
				self.treeWidget_history.topLevelItem(row).setText(0, str(tables[table][2]))
				self.treeWidget_history.topLevelItem(row).setText(1, str(tables[table][3]))
				self.treeWidget_history.topLevelItem(row).setText(2, str(tables[table][4]))
				self.treeWidget_history.topLevelItem(row).setText(3, str(tables[table][5]))
				self.treeWidget_history.topLevelItem(row).setText(4, str(tables[table][6]))
				self.treeWidget_history.topLevelItem(row).setText(5, str(tables[table][7]))
				for column in range(len(displayed_columns)):
					self.treeWidget_history.topLevelItem(row).setTextAlignment(column, qc.Qt.AlignCenter)
		self.treeWidget_history_errorNotes.clear()
		for table in range(len(tables)):
			if tables[table][1]-1 == getRow:
				qg.QTreeWidgetItem(self.treeWidget_history_errorNotes)
				row = self.treeWidget_history_errorNotes.topLevelItemCount()-1
				self.treeWidget_history_errorNotes.topLevelItem(row).setText(0, str(tables[table][10]))
				self.treeWidget_history_errorNotes.topLevelItem(row).setTextAlignment(0, qc.Qt.AlignCenter)
             			
	def createTable_by_smartsheetData(self):
		newDate = datetime.now().strftime("%Y-%m-%d")
		newTime = datetime.now().strftime("%H:%M:%S")
		newArtist = getpass.getuser()       
		columns = self.DB.GetColumns()
		getSmartsheetData = SmartsheetData('1n88t5e1kood6tpr22j3ohpi3g')
		#smartsheetData[0] == shot,smartsheetData[1] == start frame,smartsheetData[2] == end frame		
		smartsheetData = getSmartsheetData.getCellData("%s - Animation"%("CML113"), "CML_", "Sc Brkdwn", "Strt Frame", "End Frame")
		"""for column in range(len(columns)):
			if columns[column][0] != "Error_Notes":
				self.tableWidget_data.setColumnCount(column+1)
				self.tableWidget_data.setHorizontalHeaderLabels([col[0] for col in columns])
		for row, table_shot, table_startFrame, table_endFrame in zip(range(len(smartsheetData[0])), smartsheetData[0], smartsheetData[1], smartsheetData[2]):
			self.tableWidget_data.setRowCount(row+1)
			for column in range(len(columns)):
				if columns[column][0] != "Error_Notes":
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "ID":
						self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(row+1)))
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "ID_History":
						self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(row+1)))
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Shot":
						self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(table_shot)))
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Date":
						self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(newDate)))	
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Time":
						self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(newTime)))
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Start_Frame":
						self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(table_startFrame)))
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "End_Frame":
						self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(table_endFrame)))
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Artist":
						self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(newArtist)))			
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Mastershot":				
						comboBox = CustomComboBox()
						#comboBox.setSizeAdjustPolicy(comboBox.AdjustToContents)						
						comboBox.addItem(qc.QString(""))					
						comboBox.addItem(qg.QIcon("A:/Ticklers/Chameleon/MySQL/icon/correct.png"), qc.QString("                 YES"))
						comboBox.setIconSize(qc.QSize(70,16))
						self.tableWidget_data.setCellWidget(row, column, comboBox)
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Status":
						self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str("No Status")))	
					try:
						self.tableWidget_data.item(row, column).setTextAlignment(qc.Qt.AlignCenter)
					except:
						pass"""

	def updateCheckBox(self):	 
		updateTable = UpdateTable()
		id_updateCheckBox = updateTable.updateCheckBox('headerFilter_ID', self.checkBox_id)
		idHistory_updateCheckBox = updateTable.updateCheckBox('headerFilter_ID_History', self.checkBox_id_history)
		shot_updateCheckBox = updateTable.updateCheckBox('headerFilter_Shot', self.checkBox_shot)
		date_updateCheckBox = updateTable.updateCheckBox('headerFilter_Date', self.checkBox_date)
		time_updateCheckBox = updateTable.updateCheckBox('headerFilter_Time', self.checkBox_time)
		artist_updateCheckBox = updateTable.updateCheckBox('headerFilter_Artist', self.checkBox_artist)
		startFrame_updateCheckBox = updateTable.updateCheckBox('headerFilter_Start_Frame', self.checkBox_startFrame)
		endFrame_updateCheckBox = updateTable.updateCheckBox('headerFilter_End_Frame', self.checkBox_endFrame)
		mastershot_updateCheckBox = updateTable.updateCheckBox('headerFilter_Mastershot', self.checkBox_mastershot)
		status_updateCheckBox = updateTable.updateCheckBox('headerFilter_Status', self.checkBox_status)

	def updateTable(self):	 
		updateTable = UpdateTable()
			
		if self.checkBox_artist.isChecked():
			self.toolButton_artist.setEnabled(True)
		else:
			self.toolButton_artist.setEnabled(False)

		if self.checkBox_mastershot.isChecked():
			self.toolButton_mastershot.setEnabled(True)
		else:
			self.toolButton_mastershot.setEnabled(False)

		if self.checkBox_status.isChecked():
			self.toolButton_status.setEnabled(True)
		else:
			self.toolButton_status.setEnabled(False)
					
		id_updateHeaderItem = updateTable.updateHeaderItem(self.checkBox_id, "ID", 'headerFilter_ID')
		idHistory_updateHeaderItem = updateTable.updateHeaderItem(self.checkBox_id_history, "ID_History", 'headerFilter_ID_History')
		shot_updateHeaderItem = updateTable.updateHeaderItem(self.checkBox_shot, "Shot", 'headerFilter_Shot')
		date_updateHeaderItem = updateTable.updateHeaderItem(self.checkBox_date, "Date", 'headerFilter_Date')
		time_updateHeaderItem = updateTable.updateHeaderItem(self.checkBox_time, "Time", 'headerFilter_Time')
		artist_updateHeaderItem = updateTable.updateHeaderItem(self.checkBox_artist, "Artist", 'headerFilter_Artist')		
		startFrame_updateHeaderItem = updateTable.updateHeaderItem(self.checkBox_startFrame, "Start_Frame", 'headerFilter_Start_Frame')
		endFrame_updateHeaderItem = updateTable.updateHeaderItem(self.checkBox_endFrame, "End_Frame", 'headerFilter_End_Frame')
		mastershot_updateHeaderItem = updateTable.updateHeaderItem(self.checkBox_mastershot, "Mastershot", 'headerFilter_Mastershot')
		status_updateHeaderItem = updateTable.updateHeaderItem(self.checkBox_status, "Status", 'headerFilter_Status')
		tree.write(giggleManager_fullPath)
		#[0] == count, [1] == label name	
		horizontalHeaderCount = (id_updateHeaderItem[0] + idHistory_updateHeaderItem[0] + shot_updateHeaderItem[0] + date_updateHeaderItem[0] + time_updateHeaderItem[0] +\
								artist_updateHeaderItem[0] + startFrame_updateHeaderItem[0] + endFrame_updateHeaderItem[0] + mastershot_updateHeaderItem[0] +\
								status_updateHeaderItem[0])
		horizontalHeaderLabel = [id_updateHeaderItem[1], idHistory_updateHeaderItem[1], shot_updateHeaderItem[1], date_updateHeaderItem[1], time_updateHeaderItem[1], \
								artist_updateHeaderItem[1], startFrame_updateHeaderItem[1], endFrame_updateHeaderItem[1], mastershot_updateHeaderItem[1], \
								status_updateHeaderItem[1]]
		columns = self.DB.GetColumns()
		rows = self.DB.GetTable()
		self.tableWidget_data.setSelectionMode(qg.QAbstractItemView.ExtendedSelection)
		for column in range(horizontalHeaderCount):
			self.tableWidget_data.setSortingEnabled(False)
			self.tableWidget_data.setColumnCount(column+1)
		labels = [labels for labels in horizontalHeaderLabel if labels != None]
		self.tableWidget_data.setHorizontalHeaderLabels([label for label in labels])

		row_list = []
						
		for col in range(len(columns)):
			if columns[col][0] == "Status":
				for row in rows:
					for item in self.listWidget_bodyFilter.selectedItems():
						if row[col] == item.text():
							row_list.append(row)
		
				
		"""for row in range(len(row_list)):
			print "AAA"
			if row_list != []:
				self.tableWidget_data.setRowCount(range(len(row_list))+1)
			else:
				self.tableWidget_data.setRowCount(row+1)"""
		
		if row_list == []:
			for row in range(len(rows)):
				self.tableWidget_data.setRowCount(row+1)
				for column in range(len(horizontalHeaderLabel)):
					try:	
						if self.checkBox_id.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "ID":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(row+1)))
						elif self.checkBox_id_history.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "ID_History":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(row+1)))			    
						elif self.checkBox_shot.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Shot":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][2])))
						elif self.checkBox_date.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Date":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][3])))
						elif self.checkBox_time.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Time":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][4])))
						elif self.checkBox_artist.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Artist":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][5])))							
						elif self.checkBox_startFrame.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Start_Frame":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][6])))
						elif self.checkBox_endFrame.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "End_Frame":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][7])))
						elif self.checkBox_mastershot.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Mastershot":
							comboBox = CustomComboBox()					
							comboBox.addItem(qc.QString(""))					
							comboBox.addItem(qg.QIcon("A:/Ticklers/Chameleon/MySQL/icon/correct.png"), qc.QString("                 YES"))
							comboBox.setIconSize(qc.QSize(70,16))
							comboBox.setCurrentIndex(rows[row][8])
							self.tableWidget_data.setCellWidget(row, column, comboBox)
						elif self.checkBox_status.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Status":
							#self.tableWidget_data.setRowCount(row+1)	
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][9])))
							self.tableWidget_data.item(row, column).setTextAlignment(qc.Qt.AlignCenter)		
						else:
							self.tableWidget_data.setColumnCount(0)
						self.tableWidget_data.item(row, column).setTextAlignment(qc.Qt.AlignCenter)      				        
					except:
						pass
					
			self.setStatusColor()
			self.setArtistColor()
		else:
			for row in range(len(row_list)):
				self.tableWidget_data.setRowCount(row+1)
				for column in range(len(horizontalHeaderLabel)):
					try:	
						if self.checkBox_id.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "ID":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(row+1)))
						elif self.checkBox_id_history.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "ID_History":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(row+1)))			    
						elif self.checkBox_shot.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Shot":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][2])))
						elif self.checkBox_date.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Date":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][3])))
						elif self.checkBox_time.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Time":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][4])))
						elif self.checkBox_artist.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Artist":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][5])))							
						elif self.checkBox_startFrame.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Start_Frame":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][6])))
						elif self.checkBox_endFrame.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "End_Frame":
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][7])))
						elif self.checkBox_mastershot.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Mastershot":
							comboBox = CustomComboBox()					
							comboBox.addItem(qc.QString(""))					
							comboBox.addItem(qg.QIcon("A:/Ticklers/Chameleon/MySQL/icon/correct.png"), qc.QString("                 YES"))
							comboBox.setIconSize(qc.QSize(70,16))
							comboBox.setCurrentIndex(rows[row][8])
							self.tableWidget_data.setCellWidget(row, column, comboBox)
						elif self.checkBox_status.isChecked() and self.tableWidget_data.horizontalHeaderItem(column).text() == "Status":
							#self.tableWidget_data.setRowCount(row+1)	
							self.tableWidget_data.setItem(row, column, qg.QTableWidgetItem(str(rows[row][9])))
							self.tableWidget_data.item(row, column).setTextAlignment(qc.Qt.AlignCenter)		
						else:
							self.tableWidget_data.setColumnCount(0)
						self.tableWidget_data.item(row, column).setTextAlignment(qc.Qt.AlignCenter)      				        
					except:
						pass
					
			self.setStatusColor()
			self.setArtistColor()
					
	def saveTable(self):
		# [0] = id, [1] = id_history, [2] = shot, [3] = date, [4] = time, [5] = artist_name
		# [6] = start_frame, [7] = end_frame, [8] = mastershot, [9] = status
		columns = self.DB.GetColumns()
		tables = self.DB.GetTable()
		if tables == []:
			rowCount = self.tableWidget_data.rowCount()
			columnCount = self.tableWidget_data.columnCount()
			for row in range(rowCount):
				for column in range(columnCount):
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "ID_History":
						idHistory = self.tableWidget_data.item(row,column).text()
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Shot":
						shots = self.tableWidget_data.item(row,column).text()      				
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Start_Frame":
						startFrame = self.tableWidget_data.item(row,column).text() 
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "End_Frame":
						endFrame = self.tableWidget_data.item(row,column).text()    
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Mastershot":
						mastershot = self.tableWidget_data.cellWidget(row,column).currentIndex() 
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Status":
						status = self.tableWidget_data.item(row,column).text()
						errorNotes = None  				    				    				     				
						self.DB.AddEntryToTable(int(idHistory), shots, int(startFrame), int(endFrame), int(mastershot), status, errorNotes)
		else:
			rowCount = self.tableWidget_data.rowCount()
			columnCount = self.tableWidget_data.columnCount()
			modifiedRow_list = [] 
			for row in range(rowCount):
				for column in range(columnCount):
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Mastershot" and self.tableWidget_data.cellWidget(row,column).currentIndex() != tables[row][8]:
						mastershot = self.tableWidget_data.cellWidget(row,column).currentIndex()
						self.DB.UpdateEntryToTable_mastershot(mastershot, row+1)
					if self.tableWidget_data.horizontalHeaderItem(column).text() == "Status" and self.tableWidget_data.item(row,column).text() != tables[row][9]:
						status = self.tableWidget_data.item(row,column).text()
						self.DB.UpdateEntryToTable_status(status, row+1)
					
		self.DB.CreateTable()
						
#-----------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

def createWindows():
	global dialog
	try:
		dialog.close()
	except:
		pass
	dialog = MyDatabase(schema, table, tableLH)
	dialog.show()


schema = 'chameleon'
table = 'lighting'
tableLH = 'lighting_history'

createWindows()