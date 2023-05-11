import os
import discord
import datetime
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!help for commands"))
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    await member.guild.system_channel.send(f'Welcome {member.mention} to our server!')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')
    except Exception as e:
        await ctx.send(str(e))

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')
    except Exception as e:
        await ctx.send(str(e))

@bot.command()
async def testban(ctx):
    await ctx.send("To ban a user, type: `!ban @username [reason]`. Replace `@username` with the user's username and `[reason]` with the reason for the ban.")

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
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
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
        embed.set_thumbnail(url=f"{member.display_avatar.url}")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(str(e))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == 'hello bot':
        response = "Hi there!"
        await message.channel.send(response)
    await 
        bot.process_commands(message)

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="A new poll has been created!", description=f"{question}", color=discord.Color.dark_teal())
    embed.set_footer(text=f"Poll created by: {ctx.author.display_name}")
    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')
    await message.add_reaction('👎')

bot.run(os.environ["DISCORD_TOKEN"])

