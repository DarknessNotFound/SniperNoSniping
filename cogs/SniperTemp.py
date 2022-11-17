import discord
from discord.ext import commands
from funcs import accessible_channel
from datetime import datetime
from CRUD import *

class SnipeTemp_Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
    # Commands
    @commands.command(name='snipe', help='Adds a snipe to the database')
    async def snipe(self, ctx, *args):
        #Get who sent the message
        sniper = ctx.author.name
        
        #Get the one who was sniped
        sniped = ' '.join(args)

        #Get the time
        timestamp = datetime.now()
        #Add the sniped to the database and send confirmation message
        if(AddTempSnipe(sniper, sniped, timestamp) == True):
            await ctx.send(f"{sniper} sniped {sniped}  successfully at {timestamp}!")
        else:
            await ctx.send(f"{sniper} sniping {sniped} failed to add to database... please try again")

    @commands.command(name='AllSnipes', help='Shows all of the snipes in the database. Can do ">>AllSnipes today" to show todays snipes. Can add a number as an argument to show snipes from x days ago: ">>AllSnipes x".')
    async def AllSnipes(self, ctx, *args):
        print("AllSnipes executed")

        if IsAdmin(ctx.author.name) == False:
            await ctx.send("You don't have access to that command")
            return

        try:
            Conn = sqlite3.connect(GetDbName())
            Cur = Conn.cursor()

            if(len(args) == 0):
                data = Cur.execute("SELECT * FROM TempSnipes;")
            elif(len(args) == 1):
                if(args[0].lower() == "today"):
                    data = Cur.execute("SELECT * FROM TempSnipes WHERE Timestamp > DATE('now', 'localtime');")
                else:
                    if(len(args[0]) <= 2):
                        data = Cur.execute(f"""
                                            SELECT * 
                                            FROM TempSnipes 
                                            WHERE Timestamp > DATE('now', 'localtime', '-{args[0]} day')
                                            AND Timestamp < DATE('now', 'localtime', '-{int(args[0]) - 1} day');
                                        """)
                    else:
                        await ctx.send("Arguments not understood or too many args, sending snipes from today instead...")
                        data = Cur.execute("SELECT * FROM TempSnipes WHERE Timestamp > DATE('now', 'localtime');")                        
            else:
                await ctx.send("Arguments not understood or too many args, sending snipes from today instead...")
                data = Cur.execute("SELECT * FROM TempSnipes WHERE Timestamp > DATE('now', 'localtime');")

            await ctx.send("Format: (Id, Sniper, Sniped, Timestamp)")
            if(data.rowcount <= 0):
                await ctx.send("No data found...")

            for row in data:
                await ctx.send(row)
        except Exception as ex:
            print(f"SnipeTemp_Commands -- AllSnipes -- {ex}")
        finally:
            Conn.close()
            print("AllSnipes finished execution")

    @commands.command(name='SnipesToday', help='Shows all of the snipes from today.')
    async def SnipesToday(self, ctx, *args):
        print("SnipesToday executed")

        try:
            Conn = sqlite3.connect(GetDbName())
            Cur = Conn.cursor()
            data = Cur.execute("SELECT * FROM TempSnipes WHERE Timestamp > DATE('now', 'localtime')")
            
            await ctx.send("Format: (Id, Sniper, Sniped, Timestamp)")
            for row in data:
                await ctx.send(row)
        except Exception as ex:
            print(f"SnipeTemp_Commands -- AllSnipes -- {ex}")
        finally:
            Conn.close()
            print("SnipesToday finished execution")

    @commands.command(name='AmountOfSnipes', help='Shows the total number of snipes in the database.')
    async def AmountOfSnipes(self, ctx, *args):
        print("AmountOfSnipes executed")
        try:
            Conn = sqlite3.connect(GetDbName())
            Cur = Conn.cursor()

            data = Cur.execute("SELECT * FROM TempSnipes;")

            await ctx.send(f"Snipes this season: {data.rowcount}")

        except Exception as ex:
            print(f"SnipeTemp_Commands -- AmountOfSnipes -- {ex}")
        finally:
            Conn.close()
            print("AmountOfSnipes finished execution")

    @commands.command(name='AllSnipers', help='Gets all the names of all the snipers')
    async def AllSnipers(self, ctx, *args):
        print("AllSnipers executed")

        if IsAdmin(ctx.author.name) == False:
            await ctx.send("You don't have access to that command")
            return

        try:
            Conn = sqlite3.connect(GetDbName())
            Cur = Conn.cursor()
            data = Cur.execute(f"SELECT DISTINCT Sniper FROM TempSnipes")

            if data is None:
               ctx.send("No snipers in database found")

            for row in data:
                msg = f"{row[0]} -- Snipes: "
                Cur = Conn.cursor()
                SnipeNum = Cur.execute(f"SELECT COUNT(*) FROM TempSnipes WHERE Sniper = '{row[0]}'")
                for count in SnipeNum:
                    msg += f"{count[0]} "
                await ctx.send(msg)

        except Exception as ex:
            print(f"SnipeTemp_Commands -- AllSnipes -- {ex}")
        finally:
            Conn.close()
            print("AllSnipers finished execution")

    @commands.command(name='SnipesFrom', help='Gets all of the snipes from a single player')
    async def SnipesFrom(self, ctx, *args):
        print("SnipesFrom executed")

        if IsAdmin(ctx.author.name) == False:
            await ctx.send("You don't have access to that command")
            return

        try:
            Conn = sqlite3.connect(GetDbName())
            Cur = Conn.cursor()
            data = Cur.execute(f"SELECT * FROM TempSnipes WHERE Sniper = '{' '.join(args)}'")

            if data is None:
                ctx.send("That sniper has not made any snipes. You might have also misspelled the name, use >>AllSnipers.")

            for row in data:
                await ctx.send(row)
        except Exception as ex:
            print(f"SnipeTemp_Commands -- SnipesFrom -- {ex}")
        finally:
            Conn.close()
            print("SnipesFrom finished execution")

    @commands.command(name='SnipeId', help='Gets snipe information based on id number.')
    async def SnipeId(self, ctx, *args):
        print("SnipeId executed")
        try:
            Conn = sqlite3.connect(GetDbName())
            Cur = Conn.cursor()
            data = Cur.execute(f"SELECT * FROM TempSnipes WHERE Id = '{' '.join(args)}'")

            if data is None:
                ctx.send(f"That snipe id '{' '.join(args)}' is invalid.")

            for row in data:
                await ctx.send(row)
        except Exception as ex:
            print(f"SnipeTemp_Commands -- SnipeId -- {ex}")
        finally:
            Conn.close()
            print("SnipeId finished execution")

    @commands.command(name='AllSniped', help='Gets all of the people who have been sniped')
    async def AllSniped(self, ctx, *args):
        if IsAdmin(ctx.author.name) == False:
            await ctx.send("You don't have access to that command")
            return

        try:
            Conn = sqlite3.connect(GetDbName())
            Cur = Conn.cursor()
            data = Cur.execute(f"SELECT DISTINCT Sniped FROM TempSnipes")

            if data is None:
                ctx.send("No snipes found")

            for row in data:
                msg = f"{row[0]} -- Sniped: "
                Cur = Conn.cursor()
                SnipeNum = Cur.execute(f"SELECT COUNT(*) FROM TempSnipes WHERE Sniped = '{row[0]}'")
                for count in SnipeNum:
                    msg += f"{count[0]} "
                await ctx.send(msg)
        except Exception as ex:
            print(f"SnipeTemp_Commands -- SnipesFrom -- {ex}")
        finally:
            Conn.close()

    @commands.command(name='SnipingSeason', help='Shows an announcement for the start of sniping season')
    async def SnipingSeason(self, ctx, *args):
        print("Started Sniping Season")

        if IsAdmin(ctx.author.name) == False:
            await ctx.send("You don't have access to that command")
            return
        
        embed=discord.Embed(
                title="Swiper no swiping, Swiper no swiping, Swiper...",
                description="I'm sick and tired of this *stupid little brat* being able to stop **me** from doing what I want. Dora wanted an adventure and I intend to give her one.",
                color=discord.Color.green())
        embed.add_field(name="I need help", value="I need someone to take out this Dora, someone who can finish her quickly, quietly, and with a bang. She won't even have time to say Sniper No Sniping.", inline=False)
        embed.add_field(name="Try outs begin now", value="You have from now through November to impress me and my panel of judges. Use the `>>snipe @Person` and post the picture to let my judges know when you get someone.")
        embed.add_field(name="Payment", value="I will give a prize to the one who has the most snipes and a compensation to the one who got sniped the most.")
        embed.add_field(name="Happy Hunting", value="Dora's next adventure will *clear* her head.", inline=False)
        embed.set_footer(text="NOTE: if the person isn't in the discord but is a legal snipe, use their first and last name to help the moderators count snipes at the end of the season.")
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(SnipeTemp_Commands(client))
