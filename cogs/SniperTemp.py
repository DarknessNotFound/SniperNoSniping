import discord
from discord.ext import commands
from funcs import accessible_channel
from SniperFuncs import *
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
		AddTempSnipe(sniper, sniped, timestamp)
		await ctx.send(SniperMessage(sniper, sniped, timestamp))

async def setup(client):
	await client.add_cog(SnipeTemp_Commands(client))
