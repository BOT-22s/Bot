import os
import discord
import datetime
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!help for commands"))
    print(f"Logged in as {bot.user}")


@bot.event
async def on_member_join(member):
    welcome_channel = member.guild.system_channel
    if welcome_channel is not None:
        await welcome_channel.send(f'Welcome {member.mention} to our server!')


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')
    except discord.Forbidden:
        await ctx.send("I don't have permission to ban members.")
    except Exception as e:
        await ctx.send(str(e))


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')
    except discord.Forbidden:
        await ctx.send("I don't have permission to kick members.")
    except Exception as e:
        await ctx.send(str(e))


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    try:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Cleared {amount} messages.', delete_after=5)
    except discord.Forbidden:
        await ctx.send("I don't have permission to manage messages.")
    except Exception as e:
        await ctx.send(str(e))


@bot.command()
async def testban(ctx):
    await ctx.send("To ban a user, type: `.ban @username [reason]`. Replace `@username` with the user's username and `[reason]` with the reason for the ban.")


@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000
    await ctx.send(f'Pong! Latency: {latency:.2f} ms')


@bot.command()
async def hello(ctx):
    await ctx.send("Choo choo! 🚅")


@bot.command()
async def info(ctx):
    try:
        embed = discord.Embed(
            title=f"{ctx.guild.name}",
            description="Lorem Ipsum asdasd",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.blue()
        )
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
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required arguments.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument passed.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")


@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(
        title=f"{member}",
        description=f"Here is the info we retrieved about the user {member.mention}",
        color=discord.Color.dark_blue()
    )
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Nickname", value=member.nick, inline=True)
    embed.add_field(name="Created at", value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline=False)
    embed.add_field(name="Joined at", value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline=False)
    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == 'hello bot':
        response = "Hi there!"
        await message.channel.send(response)

    await bot.process_commands(message)


@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(
        title="A new poll has been created!",
        description=f"{question}",
        color=discord.Color.dark_teal()
    )
    embed.set_footer(text=f"Poll created by: {ctx.author.display_name}")
    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')
    await message.add_reaction('👎')


@bot.command()
async def greet(ctx, member: discord.Member):
    await ctx.send(f"Hello {member.mention}!")


@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    roles = ", ".join([role.name for role in guild.roles if role.name != "@everyone"])
    emojis = ", ".join([str(emoji) for emoji in guild.emojis])
    online_members = len([member for member in guild.members if member.status != discord.Status.offline])

    embed = discord.Embed(title="Server Information", color=discord.Color.green())
    embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Owner", value=guild.owner, inline=False)
    embed.add_field(name="Region", value=guild.region, inline=False)
    embed.add_field(name="Created at", value=guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline=False)
    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    embed.add_field(name="Online Members", value=online_members, inline=False)
    embed.add_field(name="Roles", value=roles, inline=False)
    embed.add_field(name="Emojis", value=emojis, inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title="Avatar", color=discord.Color.blue())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)


bot.run(os.environ["DISCORD_TOKEN"])
