import os
import discord
import datetime
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!help for commands"))
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to our Discord server!')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')
    except Exception as e:
        await ctx.send(str(e))

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def hello(ctx):
    await ctx.send("Choo choo! 🚅")

@bot.command()
async def info(ctx):
    try:
        embed = discord.Embed(title=f"{ctx.guild.name}", description="Lorem Ipsum asdasd", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
        embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
        embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
        embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(str(e))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used.")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    try:
        if not member:  # if member is not mentioned
            member = ctx.message.author  # set member as the author
        embed = discord.Embed(title=f"{member}", description=f"Here is the info we retrieved about the user {member.mention}", color=discord.Color.dark_blue())
        embed.add_field(name="ID", value=f"{member.id}", inline=True)
        embed.add_field(name="Nickname", value=f"{member.nick}", inline=True)
        embed.add_field(name="Created at", value=f"{member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC')}", inline=False)
        embed.add_field(name="Joined at", value=f"{member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC')}", inline=False)
        embed.set_thumbnail(url=f"{member.avatar_url}")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(str(e))

bot.run(os.environ["DISCORD_TOKEN"])
