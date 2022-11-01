from DB_Creation import *

TempSnipesTable = GetTempSnipesTableName()

def AddTempSnipe(Sniper, Sniped):
	try:
		Conn = sqlite3.connect(GetDbName())
		TempSnipesTable = GetTempSnipesTableName()
		
		if(TableExistsInDb(Conn, TempSnipesTable) == False):
			print("CRUD.py -- AddTempSnipe -- TempSnipesTable doesn't exist")
			return

		Conn = sqlite3.execute(
		
