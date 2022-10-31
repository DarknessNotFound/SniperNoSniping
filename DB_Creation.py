import sqlite3

def GetDbName():
	return "SniperNoSnipingDB"

def GetSnipesTableName():
	return "Snipes"

def GetPlayersTableName():
	return "Players"

def GetPlayerNameVarientTableName():
	return "PlayerNameVarients"

def SetupDB():
	try:
		Conn = sqlite3.connect(GetDbName())
		
		SnipesT = GetSnipesTableName()
		PlayerT = GetPlayersTableName()
		NameVarientT = GetPlayerNameVarientTableName()	
		
		# For each table: Check if table exists, if not, then create the table
		# and send a message that it was completed successfully.

		# Player table keeps track of each player's name, discord tag, and
		# if they are in the discord or not.
		if(TableExistsInDb(Conn, PlayerT) == False):
			Conn.execute("""
				CREATE TABLE {0}(
					Id INTEGER PRIMARY KEY AUTOINCREMENT,
					DiscordName text,
					FirstName VARCHAR(31),
					LastName VARCHAR(31),
					InDiscord INT2,
					IsDeleted INT2
				)""".format(PlayerT))
			print("{0} table created.".format(PlayerT))

		# Snipes table keeps track of who sniped who and went. This will reference the
		# player table to keep track of the "who". 
		if(TableExistsInDb(Conn, SnipesT) == False):
			Conn.execute("""
				CREATE TABLE {0}(
					Id INTEGER PRIMARY KEY AUTOINCREMENT,
					Sniper INTEGER NOT NULL,
					Sniped INTEGER NOT NULL,
					timestamp DATETIME NOT NULL,
					IsDeleted INT2,
					FOREIGN KEY(Sniper) REFERENCES {1}(Id),
					FOREIGN KEY(Sniped) REFERENCES {1}(Id)
				)""".format(SnipesT, PlayerT))
			print("{0} table created.".format(SnipesT))

	except Exception as e:
		print("DB_Creation.py -- SetupDB -- {}".format(e))

	finally:
		Conn.close()
		print("DB_Creation.py -- SetupDB -- DB closed")

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
	except:
		print("DB_Creation.py -- TableExistsInDb -- Error while checking if table exists")
		return False
