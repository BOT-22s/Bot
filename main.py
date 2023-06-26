import os
import discord
import datetime
import asyncio
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=".help for commands"))
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    welcome_channel = member.guild.system_channel
    if welcome_channel is not None:
        embed = discord.Embed(
            title=f"Welcome {member.name}!",
            description=f"Thanks for joining our server, {member.mention}!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"Joined at {member.joined_at.strftime('%a, %d %B %Y, %I:%M %p UTC')}")
        await welcome_channel.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Member Banned",
            description=f"{member.name} has been banned from the server.",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Reason", value=reason or "No reason provided.")
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("I don't have permission to ban members.")
    except Exception as e:
        await ctx.send(str(e))

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Member Kicked",
            description=f"{member.name} has been kicked from the server.",
            color=discord.Color.orange()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Reason", value=reason or "No reason provided.")
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("I don't have permission to kick members.")
    except Exception as e:
        await ctx.send(str(e))

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    try:
        await ctx.channel.purge(limit=amount + 1)
        embed = nextcord.Embed(
            title="Messages Cleared",
            description=f"{amount} messages have been cleared in this channel.",
            color=nextcord.Color.blue()
        )
        await ctx.send(embed=embed, delete_after=5)
    except nextcord.Forbidden:
        await ctx.send("I don't have permission to manage messages.")
    except Exception as e:
        await ctx.send(str(e))

@bot.command()
async def testban(ctx):
    embed = discord.Embed(
        title="How to Ban a User",
        description="To ban a user, use the command `.ban @username [reason]`.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000
    embed = discord.Embed(
        title="Ping",
        description=f"Pong! Latency: {latency:.2f} ms",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


@bot.command()
async def hello(ctx):
    embed = discord.Embed(
        title="Hello!",
        description="Choo choo! 🚅",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)


@bot.command()
async def info(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title=guild.name,
        description="Server Information",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Created at", value=guild.created_at.strftime('%a, %d %B %Y, %I:%M %p UTC'), inline=False)
    embed.add_field(name="Owner", value=guild.owner.mention, inline=False)
    embed.add_field(name="Members", value=guild.member_count, inline=False)
    embed.add_field(name="Region", value=guild.region, inline=False)
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Missing Argument",
            description="Please provide all the required arguments.",
            color=discord.Color.red()
        )
        error_message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await error_message.delete()
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="Invalid Argument",
            description="Please provide a valid argument.",
            color=discord.Color.red()
        )
        error_message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await error_message.delete()
    elif isinstance(error, discord.HTTPException):
        embed = discord.Embed(
            title="Rate Limit Exceeded",
            description="Oops! We are being rate-limited. Please try again later.",
            color=discord.Color.red()
        )
        error_message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await error_message.delete()
    else:
        embed = discord.Embed(
            title="Error",
            description=f"An error occurred: {str(error)}",
            color=discord.Color.red()
        )
        error_message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await error_message.delete()


@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(
        title="User Information",
        description=f"Here is the info we retrieved about {member.name}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Nickname", value=member.nick or "N/A", inline=True)
    embed.add_field(name="Joined at", value=member.joined_at.strftime('%a, %d %B %Y, %I:%M %p UTC'), inline=False)
    embed.add_field(name="Created at", value=member.created_at.strftime('%a, %d %B %Y, %I:%M %p UTC'), inline=False)
    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == 'hello bot':
        embed = discord.Embed(
            title="Hello!",
            description="Hi there!",
            color=discord.Color.green()
        )
        await message.channel.send(embed=embed)

    await bot.process_commands(message)


@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(
        title="📊 New Poll",
        description=question,
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Poll created by: {ctx.author.display_name}")
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction('👍')
    await asyncio.sleep(0.5)  # Add a delay between reactions
    await poll_message.add_reaction('👎')

    await ctx.message.delete()  # Delete the command message


@bot.command()
async def embed(ctx, title, description, color="blue"):
    try:
        color = getattr(discord.Color, color.lower())()
    except AttributeError:
        color = discord.Color.blue()

    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    await ctx.send(embed=embed)


@bot.command()
async def servericon(ctx):
    embed = discord.Embed(
        title="Server Icon",
        description="Here is the server icon:",
        color=discord.Color.blue()
    )
    embed.set_image(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(
        title="Avatar",
        description=f"Here is the avatar of {member.name}:",
        color=discord.Color.blue()
    )
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    link = await ctx.channel.create_invite(max_age = 300)
    await ctx.send(f"Here is an instant invite to our server: {link}")

@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)

@bot.command()
async def play(ctx, *, search):
    source = await YTDLSource.create_source(ctx, search, loop=bot.loop)
    ctx.voice_client.play(source)

@bot.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as r:
            res = await r.json()
            embed = discord.Embed(
                title=res['data']['children'][random.randint(0, 25)]['data']['title'],
                color=discord.Color.blue()
            )
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@bot.command()
async def weather(ctx, *, city: str):
    weather = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={your_api_key}')
    data = weather.json()
    embed = discord.Embed(
        title=f"Weather in {city}",
        description=f"The temperature is {data['main']['temp']}°C, "
                    f"the weather condition is {data['weather'][0]['description']}.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

bot.run(os.environ["DISCORD_TOKEN"])
