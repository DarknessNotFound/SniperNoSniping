from DB_Creation import *

TempSnipesTable = GetTempSnipesTableName()

def AddTempSnipe(Sniper, Sniped, Timestamp):
    result = False
    try:
        Conn = sqlite3.connect(GetDbName())
        Cur = Conn.cursor()
        TempSnipesTable = GetTempSnipesTableName()

        if(TableExistsInDb(Conn, TempSnipesTable, False) == False):
            print("CRUD.py -- AddTempSnipe -- TempSnipesTable doesn't exist")
            return -1

        sql = f"""
                INSERT INTO {TempSnipesTable}(Sniper, Sniped, Timestamp)
                VALUES (?, ?, ?);
              """
        Cur.execute(sql, (Sniper, Sniped, Timestamp))
        Conn.commit()
        result = True
    except Exception as ex:
        print(f"CRUD -- AddTempSnipe -- {ex}")

    finally:
        Conn.close()
        return result

def RemoveSnipe(Id):
    try:
        Conn = sqlite3.connect(GetDbName())
        Cur = Conn.cursor()
        TempSnipesTable = GetTempSnipesTableName()

        if(TableExistsInDb(Conn, TempSnipesTable, False) == False):
            print("CRUD.py -- RemoveSnipe -- TempSnipesTable doesn't exist")
            return

        sql = f"""DELETE FROM {TempSnipesTable}
                  WHERE Id = {Id};"""

        Cur.execute(sql)
        Conn.commit()
        print("RemoveSnipe executed")
    except Exception as ex:
        print(f"CRUD -- AddTempSnipe -- {ex}")

    finally:
        Conn.close()

def UpdateSnipedSQL(Id, NewName):
    print(f"Attempting to update {Id} to Sniped = {NewName}")
    try:
        Conn = sqlite3.connect(GetDbName())
        Cur = Conn.cursor()
        TempSnipesTable = GetTempSnipesTableName()

        if(TableExistsInDb(Conn, TempSnipesTable, False) == False):
            print("CRUD.py -- RemoveSnipe -- TempSnipesTable doesn't exist")
            return

        sql = f"""
                UPDATE {TempSnipesTable}
                SET Sniped = '{NewName}'
                WHERE Id = '{Id}';
            """

        Cur.execute(sql)
        Conn.commit()
        print("RemoveSnipe executed")
    except Exception as ex:
        print(f"CRUD -- UpdateSnipe -- {ex}")

    finally:
        Conn.close()
