import discord
from discord.ext import commands
from funcs import accessible_channel
from datetime import datetime
from CRUD import *

class SnipeAdmin_Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
    # Commands
    @commands.command(name='Remove', help='Removes a snipe based on the Id inputed')
    async def Remove(self, ctx, *args):
        print("Removal executed")
        if IsAdmin(ctx.author.name) == False:
            await ctx.send("You don't have access to that command")
            return

        RemoveSnipe(''.join(args))
    
    @commands.command(name='UpdateSniped', help='Updates the person sniped based on Id')
    async def UpdateSniped(self, ctx, *args):
        print("Update called: " + ' '.join(args))
        if IsAdmin(ctx.author.name) == False:
            await ctx.send("You don't have access to that command")
            return
        
        UpdateSnipedSQL(args[0], args[1])
        try:
            Conn = sqlite3.connect(GetDbName())
            Cur = Conn.cursor()
            data = Cur.execute(f"SELECT * FROM TempSnipes WHERE Id = '{args[0]}'")

            if data is None:
                ctx.send("That sniper has not made any snipes. You might have also misspelled the name, use >>AllSnipers.")

            for row in data:
                await ctx.send(row)
        except Exception as ex:
            print(f"SnipeTemp_Commands -- UpdateSniped -- {ex}")
        finally:
            Conn.close()
            print("Finished Update called.")

async def setup(client):
    await client.add_cog(SnipeAdmin_Commands(client))
