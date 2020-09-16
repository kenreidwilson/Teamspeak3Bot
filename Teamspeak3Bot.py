import datetime
import asyncio
import aiohttp
import time
import sys
from discord.ext.commands import Bot
from discord.errors import LoginFailure

CHANNEL_ID = 750768366116929676
bot = Bot(command_prefix='!')

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
		except LoginFailure:
			print("Discord login failed: Invalid bot token.")
			sys.exit(1)
		except KeyboardInterrupt:
			print("\nExitting Gracefully")
			bot.loop.run_until_complete(bot.close())
			sys.exit(0)

@bot.event
async def on_voice_state_update(member, before, after):
	if before.channel != after.channel:
		timestamp = datetime.datetime.now().strftime("%H:%M:%S")
		if before.channel == None:
			await bot.get_channel(CHANNEL_ID).send(f':information_source: <{timestamp}> **"{member}"** connected to channel **"{after.channel}"**')
		elif after.channel != None:
			await bot.get_channel(CHANNEL_ID).send(f':information_source: <{timestamp}> **"{member}"** left heading to channel **"{after.channel}"**')
		else:	
			await bot.get_channel(CHANNEL_ID).send(f':information_source: <{timestamp}> **"{member}"** disconnected (leaving)')

@bot.event
async def on_ready():
	print(bot.user.name + " is online.\n")

if __name__ == '__main__':
	main()