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
        print("AllSnipes executed")
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
            print("AllSnipes finished execution")

    @commands.command(name='SnipingSeason', help='Shows an announcement for the start of sniping season')
    async def SnipingSeason(self, ctx, *args):
        print("Started Sniping Season")
        # if ctx.author.name != 'GmanBeCrazy':
        if False:
            await ctx.send("This command is too powerful for you to use!")
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
