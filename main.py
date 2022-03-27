from discord.ext import commands
import os
import discord
import json
import requests
import web
import random
from flames import flames_function


my_secret = os.environ['token']
my_secret_2 = os.environ['weatherapi']
my_secret_3 = os.environ['gif_api']
weather_key = os.environ['weather_api']


key_gif = my_secret_3

lmt = 8

client = commands.Bot(command_prefix = ["H "])

response_words = ['h']

encourage = ["It's ok to feel low, this will too pass", "just take a deep breath and think about the good times", "you've made it this far- why not more?", "hope shall raise in the minds and faith in hearts, for as everything happens for a reason", "you're not alone when you have yourself so believe in yourself"]
swear_words = ['dog', 'cat']
trigger_words = ['leader', "boss", 'windy']
sad_words = ["sad", 'depressed', 'lonely', 'anxious', 'suicidal', 'stressful']

limit = 3
api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)

# on ready
@client.event
async def on_ready():
  print("ready")

# error handling
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.channel.send(f"{ctx.author.mention} you cannot do that")
    await ctx.message.delete()
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.channel.send("Please fill in all the arguments")
  if isinstance(error, commands.CommandNotFound):
    return 
    
@client.event
async def on_message(msg):
  if msg.author == client.user:
    return
  
  # word filter 
  if any(word in msg.content for word in swear_words):
    mute_channel = client.get_channel(943828272830107678)
    embed_mute = discord.Embed(title = "Slur logs", description = f"User {msg.author.mention} used a slur word in  {msg.channel.mention}.", color = msg.author.color)
    await mute_channel.send(embed = embed_mute)
    await msg.delete()
    await msg.channel.send(f"{msg.author.mention} stop using slur words!!")
    await msg.author.send("Don't use slur words")
  # encouraging
  if any(word in msg.content for word in sad_words):
    encouragement = random.choice(encourage)
    await msg.channel.send(encouragement)
   
  # ping manager
  if any(word in msg.content for word in trigger_words):
    leader = await client.fetch_user(855056698842415114)
    embed = discord.Embed(title =" PING LOG", description = f"User {msg.author.mention} used mentioned you in {msg.channel.mention}, content: '{msg.content}'", color = leader.color)
    embed.set_thumbnail(url = leader.avatar_url)
    await leader.send(embed = embed)

    
  await client.process_commands(msg)

# deleting messages
@client.command(aliases = ["del"])
@commands.has_permissions(manage_messages = True)
async def delete_func(ctx, amt=1):
  await ctx.channel.purge(limit = amt+1)
  print("Messages have been deleted successfully")

  
# announcing function
@client.command(aliases = ["announce"])
@commands.has_permissions(manage_messages = True)
async def announce_func(ctx, title ,*, description):
  await ctx.message.delete()
  user = ctx.author
  embed = discord.Embed(title = title, description = description, color = user.color )
  embed.set_thumbnail(url = user.avatar_url)
  await ctx.send(embed = embed)
  print("Message has been announced")

  
#gif
@client.command()
async def gif(ctx, *, term):
  r = requests.get("https://g.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (term, key_gif, lmt))
  gif_1 = json.loads(r.content)
  gif_content = gif_1["results"][0]["media"][0]["tinygif"]["url"]
  await ctx.channel.send(gif_content)
  print("GIF has been successfully sent")

  
# facts
@client.command(aliases = ['fact'])
async def fact_function(ctx):
  response = requests.get(api_url, headers={'X-Api-Key': weather_key})
  json_fact = json.loads(response.text)
  await ctx.channel.send(json_fact[0]["fact"])
  print("Facts successfully sent")


#helper function
@client.command()
async def about(ctx):
  embed_about = discord.Embed(title = "HORI'S COMMANDS", description = ''' * For gifs: H gif (whatever you want without parenthesis)'''+ '\n'+ "* For weather: H weather (whaever city you want without parenthesis)"+ '\n'+ "* For random facts: H facts"+ '\n'+ 'To add slur words: H add (whateveryou want without parenthesis)'+ '\n' + '* For quotes: H quote')
  embed_about.set_thumbnail(url = ctx.author.avatar_url)  
  await ctx.channel.send(embed = embed_about)

  
# adding slur words
@client.command()
@commands.has_permissions(manage_messages = True)
async def add(ctx,*, word):
  swear_words.append(word)
  await ctx.channel.send("Word successfully added ")
  print("Slur word added")


# weather info
@client.command()
async def weather(ctx,*, city):
  request_weaher = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=26bfd75cb951c14b7bcda707fbbc14f5")
  json_weather = json.loads(request_weaher.text)
  await ctx.channel.send(f'''{json_weather["sys"]["country"]}, {json_weather['name']} , Current tempreature: {round(json_weather['main']['temp'] - 273.15)}°C , Humidity: {json_weather['main']['humidity']} , It is {json_weather["weather"][0]["main"]} right now''')
  print("Weather info successfully sent")

# quotes
@client.command()
async def quote(ctx):
  response_q = requests.get('https://zenquotes.io/api/random')
  json_q = json.loads(response_q.text)
  await ctx.channel.send(json_q[0]["q"] + '\n' + "-" + json_q[0]["a"])
  print("Quotes successfully sent")

#flames
@client.command()
async def f(ctx, first, *,second):
  await ctx.send(f"{first} and {second} are {flames_function(first, second)}")

web.keep_alive()
client.run(my_secret)
