import sqlite3

def SetupDB:
	try:
		Conn = sqlite3.connect("SniperNoSnipingDB")

def TableExistsInDb(Conn, Table):
	try:
		c = Conn.cursor()
       	        c.execute("""
            		SELECT count(name) FROM sqlite_master
            		WHERE type='table'
            		AND name='{0}'
			""".format(Table))
		if c.fetchone()[0]==1:
            		print(Table + ' table already exists')
			return True
        	else:
            		print(Table + ' table does not exist')
			return False
