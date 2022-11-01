import discord
from discord.ext import commands
from funcs import accessible_channel
from SniperFuncs import *

class Snipe_Commands(commands.Cog):
	def __init__(self, client):
		self.client = client
	# Commands
	@commands.command(name='echo', help='Echo what user inputed')
	async def echo(self, ctx, *args):
		if accessible_channel(ctx):
			await ctx.send(' '.join(args))
		else:
			await ctx.send("This isn't the time to use that!")

	@commands.command(name='snipe', help='Adds a snipe to the database')
	async def snipe(self, ctx, *args):
		#Guard clause against wrong channel.
		if accessible_channel(ctx) == False:
			await ctx.send("Please send commands in the Sniper bot channel!")
			return

		#Get who sent the message
		sniper = 'TestSniper'
		
		#Get the one who was sniped
		sniped = 'TestSnipe'

		#Get the time
		timestamp = 'timestamp'

		#Add the sniped to the database and send confirmation message
		AddSnipeRecord(sniper, sniped, timestamp)
		await ctx.send(SniperMessage(sniper, sniped, timestamp))


async def setup(client):
	await client.add_cog(Snipe_Commands(client))
