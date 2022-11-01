from DB_Creation import *

TempSnipesTable = GetTempSnipesTableName()

def AddTempSnipe(Sniper, Sniped, Datetime):
	try:
        print("Started temp snipe")
		Conn = sqlite3.connect(GetDbName())
		TempSnipesTable = GetTempSnipesTableName()
		
		if(TableExistsInDb(Conn, TempSnipesTable) == False):
			print("CRUD.py -- AddTempSnipe -- TempSnipesTable doesn't exist")
			return -1

        sql = f"""
                INSERT INTO {TempSnipesTable}(Sniper, Sniped, Timestamp)
                VALUES({Sniper}, {Sniped}, {Timestamp})
              """
        Cur = conn.cursor()
        cur.execute(sql)
        Conn.commit()
        print("Should be commited")

    except Exception as ex:
        print(f"CRUD -- AddTempSnipe -- {ex}")
