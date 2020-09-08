import asyncio, aiohttp, datetime, discord, json, os, time, sys
from pprint import pprint
from discord.ext import commands
from discord.ext.commands import Bot

CHANNEL_ID = 750768366116929676
bot = commands.Bot(command_prefix='!')

def main():
	while True:
		try:
			bot.loop.run_until_complete(bot.start(sys.argv[1]))
		except aiohttp.client_exceptions.ClientConnectorError:
			print("Could not connect to Discord, reconnecting...")
			time.sleep(10)
		except IndexError:
			print("You must enter a bot token.")
			sys.exit(1)
		except discord.errors.LoginFailure:
			print("Discord login failed: Invalid bot token.")
			sys.exit(1)
		except KeyboardInterrupt:
			print("\nExitting Gracefully")
			bot.loop.run_until_complete(bot.close())
			sys.exit(0)

@bot.event
async def on_voice_state_update(member, before, after):
	if before.channel != after.channel:
		if before.channel == None:
			await bot.get_channel(CHANNEL_ID).send(f'{member} connected to {after.channel}')
		elif after.channel != None:
			await bot.get_channel(CHANNEL_ID).send(f'{member} switched to {after.channel}')
		else:	
			await bot.get_channel(CHANNEL_ID).send(f'{member} disconnected from {before.channel}')

@bot.event
async def on_ready():
	print(bot.user.name + " is online.\n")

if __name__ == '__main__':
	main()