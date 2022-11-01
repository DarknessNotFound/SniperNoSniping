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
        #Guard clause against wrong channel.
        if accessible_channel(ctx) == False:
            await ctx.send("Please send commands in the Sniper bot channel!")
            return

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

    @commands.command(name='AllSnipes', help='Shows all of the snipes in the database')
    async def AllSnipes(self, ctx, *args):
        #Guard clause against wrong channel.
        if accessible_channel(ctx) == False:
            await ctx.send("Please send commands in the Sniper bot channel!")
            return

        try:
            Conn = sqlite3.connect(GetDbName())
            Cur = Conn.cursor()
            data = Cur.execute("SELECT * FROM TempSnipes")
            
            await ctx.send("Format: (Id, Sniper, Sniped, Timestamp)")
            for row in data:
                await ctx.send(row)
        except Exception as ex:
            print(f"SnipeTemp_Commands -- AllSnipes -- {ex}")
        finally:
            Conn.close()

    @commands.command(name='SnipingSeason', help='Shows an announcement for the start of sniping season')
    async def SnipingSeason(self, ctx, *args):
        print("Started Sniping Season")
        if ctx.author.name != 'GmanBeCrazy':
            await ctx.send("This command is too powerful for you to use!")
            return

        await ctx.send("""Swiper no swiping, Swiper no swiping, Swiper... Well I'm sick and tired of this stupid little kid being able to stop me from doing what I want. Dora wanted an adventure and I want to show her the true dangers of adventuring. Say, why don't you help me? I need someone to snipe her before she can say those magic words. Try outs begin now and last throughout November, the person who gets the most snipes I will give a prize to. The person who gets sniped the most will be given compensation so you don't sue me. Anyways, just type '>>snipe @Person' alongside the picture to snipe them and I will tell you if it counted or not. Please try to keep the naming using discords @'s if possible or use the persons real name to make it easier on my judges. Anyways, read the rules that are pinned and enjoy sniping. I can't wait those meddling kid and her stupid monkey... wait wrong show...""")

async def setup(client):
    await client.add_cog(SnipeTemp_Commands(client))
