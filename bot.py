import os
import random
import datetime

from discord.ext import commands
from dotenv import load_dotenv

AUSTIN_ID = 261235267166273536
JAKE_ID = 384859905598816266

ANIME_WORDS = [
    'anime',
    'vtuber',
    'vtubers',
    'weeb',
    'manga',
    'loli',
    'hentai',
    'voice actor',
    'va',
    'osu'
]

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

async def timeout_user(user_id, guild_id, duration):
    header = {
        'Authorization': f'Bot {bot.http.token}'
    }
    timeout = (
        datetime.datetime.utcnow() + datetime.timedelta(minutes=duration)
    ).isoformat()
    content = {
        'communication_disabled_until': timeout
    }
    url = f'https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}'
    async with bot.session.path(url, json=content, headers=header) as session:
        return session.status in range(200, 299)

@bot.command(
    help='If jake was talking about anime he deserves to be timed out'
)
async def timeout_roulette(ctx):
    messages = await ctx.channel.history(limit=3).flatten()
    rand_message = random.choice(messages)
    words = rand_message.content.split(' ')
    anime_discussed = any([word.lower() in ANIME_WORDS for word in words])
    if anime_discussed:
        content = (
            f'{rand_message.author} said {rand_message.content}\n'
            f'They talked about anime. {rand_message.author} will be timed out for 5 minutes.'
        )
        user_timeout = await timeout_user(
            user_id=rand_message.author.id,
            guild_id=ctx.guild.id,
            duration=10
        )
        if user_timeout:
            ctx.send(f'{rand_message.author} was successfully timedout')
        else:
            ctx.send(f'Something went wrong trying to timeout {rand_message.author}')
    else:
        content = (
            f'{rand_message.author} said {rand_message.content}\n'
            'They did not talk about anime'
        )
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
