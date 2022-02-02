import os
import random

from discord.ext import commands
from dotenv import load_dotenv

AUSTIN_ID = 261235267166273536
JAKE_ID = 384859905598816266

bot = commands.Bot(command_prefix='$')

@bot.command(
    help='Displays a word from jake from the past 2000 messages sent to this server',
    brief='Prints a word from jake'
)
async def word(ctx):
    messages = await ctx.channel.history(limit=2000).flatten()
    words = [msg for msg in messages if msg.author.id == JAKE_ID]
    rand_message = random.choice(words)
    content = f'On {rand_message.created_at}, Jake said: "{rand_message.content}"'
    await ctx.send(content=content)

@bot.command(
    help='Pings Jake',
    brief='Hi Jake!'
)
async def hi_jake(ctx):
    await ctx.send(content=f'Hi <@{JAKE_ID}>!')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

print('Initializing bot')
bot.run(TOKEN)
