#!/usr/bin/python

import getpass
import MySQL.mysql.connector
from MySQL.mysql.connector import errorcode
from datetime import datetime

##===============================================

class DatabaseUtility: 
	def __init__(self, database, tableName):
		self.db = database
		self.tableName = tableName

		self.cnx = MySQL.mysql.connector.connect(user = 'eduard',
									password = '1234',
									host = '192.168.11.189')
		self.cursor = self.cnx.cursor()

		self.ConnectToDatabase()
		self.CreateTable()
		
	def ConnectToDatabase(self):
		try:
			self.cnx.database = self.db
		except MySQL.mysql.connector.Error as err:
			if err.errno == errorcode.ER_BAD_DB_ERROR:
				self.CreateDatabase()
				self.cnx.database = self.db
			else:
				print(err.msg)

	def CreateDatabase(self):
		try:
			self.RunCommand("CREATE DATABASE %s DEFAULT CHARACTER SET 'utf8';" %self.db)
		except MySQL.mysql.connector.Error as err:
			print("Failed creating database: {}".format(err))

	def CreateTable(self):
		queryTable = ( "SHOW TABLES LIKE '%s'" )%(self.tableName);
		
		cmd = (" CREATE TABLE IF NOT EXISTS " + self.tableName + " ("
			" `ID` int(5) NOT NULL AUTO_INCREMENT,"
			" `ID_History` int(5) NULL,"
			" `Shot` char(50) NOT NULL,"
			" `Date` Date NOT NULL,"
			" `Time` Time NOT NULL,"
			" `Artist` char(20) NOT NULL,"			
			" `Start_Frame` int(5) NULL,"
			" `End_Frame` int(5) NULL,"
			" `Mastershot` tinyint NOT NULL,"
			" `Status` char(50) NOT NULL,"
			" `Error_Notes` char(100) NOT NULL,"
			" PRIMARY KEY (`ID`)"
			") ENGINE=InnoDB;");
		
		if self.tableName == 'lighting' and self.RunCommand(queryTable) == []:
			self.RunCommand(cmd)
			self.CreateTrigger()
		else:
			self.RunCommand(cmd)
		
	def CreateTrigger(self):	
		cmd = (" CREATE TRIGGER lighting_BEFORE_UPDATE BEFORE UPDATE ON lighting FOR EACH ROW INSERT INTO lighting_history VALUES (ID, OLD.ID_History, OLD.Shot, OLD.Date, OLD.Time, OLD.Artist, OLD.Start_Frame, OLD.End_Frame, OLD.Mastershot, OLD.Status, OLD.Error_Notes) ");
		
		self.RunCommand(cmd)
	def GetTable(self):
		self.CreateTable()
		return self.RunCommand("SELECT * FROM %s;" % self.tableName)

	def GetColumns(self):
		return self.RunCommand("SHOW COLUMNS FROM %s;" % self.tableName)

	def RunCommand(self, cmd):
		print ("RUNNING COMMAND: " + cmd)
		try:
			self.cursor.execute(cmd)
		except MySQL.mysql.connector.Error as err:
			print ('ERROR Shot: ' + str(err.msg))
			print ('WITH ' + cmd)
		try:
			msg = self.cursor.fetchall()
		except:
			msg = self.cursor.fetchone()
		return msg
		
	def AddEntryToTable(self, ID, Shot, Artist, Start_Frame, End_Frame, Mastershot, Status, Error_Notes):
		DateVar = datetime.now().strftime("%y-%m-%d")
		TimeVar = datetime.now().strftime("%H:%M:%S")
		
		cmd_1 = "INSERT INTO lighting (ID_History, Shot, Date, Time, Artist, Start_Frame, End_Frame, Mastershot, Status, Error_Notes) VALUES ('%d', '%s', '%s', '%s', '%s', '%d', '%d', '%s', '%s', '%s')" %(ID, Shot, DateVar, TimeVar, Artist, Start_Frame, End_Frame, Mastershot, Status, Error_Notes)

		
		#cmd = " INSERT INTO " + self.tableName + " (Shot, Date, Time, Artist, Status)"
		#cmd += " VALUES ('%s', '%s', '%s', '%s', '%s');" % (Shot, DateVar, TimeVar, ArtistVar, Status)
		#cmd_2 = "UPDATE lighting SET ID_History = ID WHERE ID = LAST_INSERT_ID()"
		
		self.RunCommand(cmd_1)
		#self.RunCommand(cmd_2)


	def UpdateEntryToTable(self, Date, Time, ID):
		cmd = "UPDATE lighting SET Date = ('%s'), Time = ('%s') WHERE ID=(%d)" %(Date, Time, ID)
		
		self.RunCommand(cmd)

	def UpdateEntryToTable_artist(self, Artist, ID):
		cmd = "UPDATE lighting SET Artist = ('%s') WHERE ID=(%d)" %(Artist, ID)
		
		self.RunCommand(cmd)
		
	def UpdateEntryToTable_mastershot(self, Mastershot, ID):
		cmd = "UPDATE lighting SET Mastershot = ('%d') WHERE ID=(%d)" %(Mastershot, ID)
		
		self.RunCommand(cmd)
		
	def UpdateEntryToTable_status(self, Status,  ID):
		cmd = "UPDATE lighting SET Status = ('%s') WHERE ID=(%d)" %(Status, ID)
		
		self.RunCommand(cmd)

	def UpdateEntryToTable_errorNotes(self, Error_Notes,  ID):
		cmd = "UPDATE lighting SET Error_Notes = ('%s') WHERE ID=(%d)" %(Error_Notes, ID)
		
		self.RunCommand(cmd)
		
	def __del__(self):
		self.cnx.commit()
		self.cursor.close()
		self.cnx.close()

##===============================================
##===============================================

	
