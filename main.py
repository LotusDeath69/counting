import discord
from discord.ext import commands
from replit import db 
import os 
from server import keepAlive
prefix = '%'


client = commands.Bot(command_prefix=prefix, help_command=None)

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Activity(
    type=discord.ActivityType.listening, name=f'%help in {len(client.guilds)} servers'
  ))
  print('logged in')


@client.event
async def on_message(message):

  if message.channel.name == 'counting' and message.author.bot == False:
    number = message.content
    try:
      guild = message.guild.id
      count_number = db[f'{guild}_count_number']
    except KeyError:
      count_number = 1
    
    if str(number) == str(count_number):
      await message.add_reaction('\u2705')
      db[f'{guild}_count_number'] = count_number + 1
    elif message.content.lower() == 'count reset' and message.author.guild_permissions.administrator == True:
      db[f'{guild}_count_number'] = 1
      await message.reply('sucessfully reset the counting number.')
    
    else:
      await message.delete()
      
  
@client.command()
async def test(ctx, arg):
  await ctx.reply('hello world')

keepAlive()
client.run(os.environ['TOKEN'])
