import sys
sys.path.append("A:/Ticklers/Chameleon/Smartsheet")
import smartsheet
class SmartsheetData(object):
	def __init__(self, token):
		self.token = token

	def getCellData(self, sheetName = None, startsWith = None, shotColumnName = None, startFrameColumnName = None, endFrameColumnName = None):
		row_numbers = []
		tablesShot_list = []
		tablesStartFrame_list = []
		tablesEndFrame_list = []
		ss = smartsheet.Smartsheet(self.token)
		# Get Sheet ID
		sheets = ss.Sheets.list_sheets(include_all=True)
		for sheet in sheets.data:
			if sheet.name.startswith(sheetName):
				sheetID = str(sheet.id)#, sheet.name
		# Get Column ID
		columnID = ss.Sheets.get_columns(sheetID)
		for column in columnID.data:
			if shotColumnName in column.title:
				shotColumn = column.id
			if startFrameColumnName in column.title:
				startFrameColumn = column.id
			if endFrameColumnName in column.title:
				endFrameColumn = column.id
		shotSheets = ss.Sheets.get_sheet(sheetID, column_ids = shotColumn, page_size = 150)
		startFrameSheets = ss.Sheets.get_sheet(sheetID, column_ids = startFrameColumn, page_size = 150)
		endFrameSheets = ss.Sheets.get_sheet(sheetID, column_ids = endFrameColumn, page_size = 150)
		for index, row in enumerate(shotSheets.rows):
			for cell in row.cells:
					if cell.display_value != None and index > 10 and cell.display_value.startswith(startsWith):
						row_numbers.append(row._row_number)
						tablesShot_list.append(cell.display_value)
		for index, row in enumerate(startFrameSheets.rows):
			for cell in row.cells:
					for row_number in row_numbers:
					    if row._row_number == row_number and cell.display_value != None and index > 10 and cell.display_value.isdigit():
					        tablesStartFrame_list.append(cell.display_value)
		for index, row in enumerate(endFrameSheets.rows):
			for cell in row.cells:
					for row_number in row_numbers:
					    if row._row_number == row_number and cell.display_value != None and index > 10 and cell.display_value.isdigit():
					        tablesEndFrame_list.append(cell.display_value)
		tableShot = [table_shot for table_shot in tablesShot_list if table_shot is not ""]
		tableStartFrame = [table_startFrame for table_startFrame in tablesStartFrame_list if table_startFrame is not ""]
		tableEndFrame = [table_endFrame for table_endFrame in tablesEndFrame_list if table_endFrame is not ""]
		return tableShot, tableStartFrame, tableEndFrame