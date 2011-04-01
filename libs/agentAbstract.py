import os
import ConfigParser
from const import *

class configuration:
	config_file_tables = ''
	
	def __init__(self):
		self.config_file_tables_path	= os.path.join(CONFIG_DIR, self.config_file_tables)
		self.tables		= {}
		self.lamps		= {}
		
		self.cp	= ConfigParser.ConfigParser()

class agent():

	app	= False
	
	def __init__(self):
		pass

	def set_app(self, app):
		self.app = app

	def register_events(self):
		pass

	def lamp_start_on(self):
		pass

	def lamp_falsestart_on(self):
		pass

	def lamp_table_on(self, table_no):
		pass

	def all_lamps_off(self):
		pass
		
	def quit(self):
		pass
		