import os
import discord
from discord_slash import SlashCommand
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True) # Declares slash commands through the bot.


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def hello(ctx):
    await ctx.send("Choo choo! 🚅")

@slash.slash(name="ping")
async def _ping(ctx):  # Defines a new "context" (ctx) command called "ping."
    await ctx.send(content="pong")

@slash.slash(name="hello")
async def _hello(ctx):  # Defines a new "context" (ctx) command called "hello."
    await ctx.send(content="Choo choo! 🚅")

bot.run(os.environ["DISCORD_TOKEN"])
