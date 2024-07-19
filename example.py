import discord
import asyncio
import time,datetime
import pandas as pd
from discord.ext import tasks, commands
from discord.ext.commands import Bot, Context
from discord.utils import find
import os
import platform
import requests, json
from dotenv import load_dotenv

"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents

Default Intents:
intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.emojis = True
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = True
intents.guild_typing = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.messages = True # `message_content` is required to get the content of the messages
intents.reactions = True
intents.typing = True
intents.voice_states = True
intents.webhooks = True

Privileged Intents (Needs to be enabled on developer portal of Discord), please use them only if you need them:
intents.members = True
intents.message_content = True
intents.presences = True
"""
#intents = discord.Intents.default()
#intents = discord.Intents(messages=True, guilds=True)
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.presences = True
"""
Privileged Intents (Needs to be enabled on developer portal of Discord), please use them only if you need them:
intents.members = True
intents.message_content = True
intents.presences = True
"""
bot = Bot(command_prefix="!",intents=intents)
"""
Uncomment this if you want to use prefix (normal) commands.
It is recommended to use slash commands and therefore not use prefix commands.

If you want to use prefix commands, make sure to also enable the intent below in the Discord developer portal.
"""
# intents.message_content = True


# Get environment variables (file .env)
load_dotenv()
TOKEN = os.getenv('TOKEN')
CHANNEL = os.getenv('CHANNEL')
GUILD = os.getenv('GUILD')

messages = joined = 0 #To count messages & user joined
last_disconnected = None #To check Bot disconnections
reconnected = False #To check Bot reconnections

@bot.event
async def on_ready() -> None:
    print("TOKEN : " + TOKEN)
    print('We have logged in as {0.user}'.format(bot))
    print(f'Discord version # {discord.__version__}' )
    print(f'Python version # {platform.python_version()}' )
    print(f'OS version # {platform.system()}' )


    #Print Downtime
    global reconnected, last_disconnected
    if last_disconnected is None:
        print ('total downtime: -----> 0.0')
    else:
        print(f'total downtime: ------> {(datetime.datetime.now() - last_disconnected).total_seconds()} seconds')
        last_disconnected=None

    #Bot online message
    botAvatar = bot.user.avatar.url
    embedbot = discord.Embed(
            title = f'Bot name: -> {bot.user.name}',
            description = 'The discord bot is online and it works like auto response & commands',
            colour = discord.Colour.blue()

        )
    embedbot.set_thumbnail(url=f'{botAvatar}')
    #embedbot.set_image(url=f'{botAvatar}')
    embedbot.set_footer(text='is online')


    #Check How many Servers are using this bot
    guild_count =0
    for guild in bot.guilds:
        print(f'Discord Server Name: {guild.name} -> (id Discord Server: {guild.id})')
        guild_count = guild_count + 1

    #Channel & Send Message of Bot Online
    for channel in guild.text_channels:
        if str(channel)== "general":
                print(f'Text Channel ? :  {channel}')
                await channel.send(embed=embedbot)

    print('running loop bot activities ----> ')
    status_task.start()
    
    #print('Starting inviting loop.....')
    #inviting.start()

    #Capture Stats on stats.txt file (15 minutos)
    update_stats.start()


@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',guild.text_channels)
    sys_chan = guild.system_channel

#Event when BOT is connected OK
@bot.event
async def on_connect():
    """
        The code in this event is executed when the bot is connected to Discord Server
        :NO PARAMETERS
    """
    reconnected=True
    print(time.strftime("%H:%M:%S UTC ",time.gmtime()) + f'Bot {bot.user.name} is connected to discord!!')

#Event when BOT is disconnected 
@bot.event
async def on_disconnect():
    """
        The code in this event is executed when the bot is diconnected from Discord Server (Refused)
        :NO PARAMETERS
    """
    print(time.strftime("%H:%M:%S UTC ",time.gmtime()) + f'Bot {bot.user.name} is disconnected from discord server!!')
    await bot.channel.send(f"Bot is disconnected from discord server")
    global last_disconnected, reconnected
    if reconnected:
        last_disconnected = datetime.datetime.now() #save disconnection time
        reconnected=False

#Evento when BOT is RESUMED
@bot.event
async def on_resume():
    """This event is called when the bot resumes a session."""
    print(time.strftime("%H:%M:%S UTC ",time.gmtime()) + f'Bot {bot.user.name} had <RESUMED> the session')

#Message Users on Channels 
@bot.event
async def on_message(message):
    """
        The code in this event is executed every time someone sends a message, with or without the prefix
        :param message: The message that was sent.
    """
    global messages
    messages=+1

    # we do not want the bot to reply to itself
    #print(f'Message Author : {message.author}')
    #print(f'Bot Author : {bot.user}')
    if message.author == bot.user:
        return

    await bot.process_commands(message)
    print('-------------------------')
    print('New messagen on channel')
    print(message.content)
   
    #Print message on console
    message_content = message.content
    message_author = message.author
    message_channel = message.channel
    print(time.strftime("%H:%M:%S UTC ",time.gmtime()) + f'New message -> {message_author} said: {message_content} on channel: {message_channel}')
    #message in lowercase to compare
    message.content=message.content.lower()

    #Response message (HELLO/HOLA)
    #English language
    if not message.author.bot: #Solo responder cuando NO ES un BOT el que envio el mensaje
        if message.content.startswith('hello'):
            print(f'Saying Hellow to Discord User -: {message.author.name} - id: {message.author.id}')
            await message.reply('Hello! I remind you that you are on Batallón Condor discord server! -----> the famous BCR!  ', mention_author=True)
        #Spanish language
        if message.content.startswith('hola'):
            print(f'Saying Hola al Discord User -: {message.author.name} - id: {message.author.id}')
            await message.reply('Hola! Te recuerdo que estas en el Server Discord del Batallón Condor! -----> los famosos BCR!', mention_author=True)

    
#Change ON Presences
@bot.event
async def on_presence_update(before, after):
    activity = before.activities
    activitylist = list(activity)
    #print(time.strftime("%H:%M:%S UTC ",time.gmtime()) + f'User -> {after} -> Changing On Presence Update -> BEFORE :{before.status} / AFTER :{after.status}')
    if str(before.status) != str(after.status):
        print(time.strftime("%H:%M:%S UTC ",time.gmtime()) + f'User -> {after} -> Changing On Presence Update STATUS -> BEFORE :{before.status} / AFTER :{after.status}')
        print(time.strftime("%H:%M:%S UTC ",time.gmtime()) + f'User -> {after} -> Changing On Presence Update ACTIVITY -> BEFORE :{before.activities} / AFTER :{after.activities}')

        # Channel ID general = 1214238892354699295
        channel = await bot.fetch_channel(1214238892354699295)    #insert you logging channel ID here
        await channel.send(f"""{after}'s activity changed from {before.status} to {after.status}""")

        UserAvatar = after.avatar.url
        embed = discord.Embed(title=f'Presence Update Note', description='detecting Users presence' , colour=0x14aaeb)
        embed.add_field (name=f'User change', value=f'({after})', inline=True)
        embed.add_field (name=f'Before Status', value=f'({before.status})', inline=True)
        embed.add_field (name=f'After Status', value=f'({after.status})', inline=True)
        embed.add_field (name=f'Before Activities', value=f'({before.activities})', inline=True)
        embed.add_field (name=f'After Activities', value=f'({after.activities})', inline=True)
        embed.set_thumbnail(url=f'{UserAvatar}')
        embed.set_footer(text=f"detecting user on {time.strftime("%H:%M:%S UTC ",time.gmtime())}")
        await channel.send(embed=embed)


#Change Status Task of BOT BCR
@tasks.loop()
async def status_task() -> None:
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(" with electricity ⚡"))
    await asyncio.sleep(60)
    await bot.change_presence(activity=discord.Streaming(name="Official Server With Dedication 🥰", url="https://zealtyro.com"))
    await asyncio.sleep(60)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="commands | Type !help for help 💁"))
    await asyncio.sleep(60)
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="all members enjoying my shocks 😳"))
    await asyncio.sleep(60)
    await bot.change_presence(activity=discord.Streaming(name='a video', url='https://www.youtube.com/'))
    await asyncio.sleep(60)
    await bot.change_presence(status=discord.Status.offline) #discord.Status.invisible
    await asyncio.sleep(60)


#Event of Message Deleted
@bot.event
async def on_message_delete(message):
    #Mention the who's message got deleted, and send the content
    await message.channel.send (f'Todos estamso viendote :eyes: {message.author.mention}: {message.content}')

#Joining to Discord Server event
@bot.event
async def on_member_join(member):
    global joined
    joined=+1
 
    #Give welcome only to NEW members
    print(time.strftime("%H:%M:%S UTC ",time.gmtime()) + f'{member} ({member.id}) ({member.display_name}) se ha unido al discord server')
    
    msgchannel = member.guild.system_channel

    for channel in member.guild.channels:
        if str(channel)== "general":

            Avatar = member.avatar.url
            embed = discord.Embed(title=f'Bienvenida!!!', description='nuevo ingreso al discord' , colour=0x14aaeb)
            embed.add_field (name=f'Se ha unido un nuevo integrante', value=f'({member})', inline=True)
            embed.set_thumbnail(url=f'{Avatar}')
            embed.set_footer(text="aviso")
            await msgchannel.send(embed=embed)
        

#Remove Users of Discord Server
@bot.event
async def on_member_remove(member):
    global joined
    joined=-1
    #Count members of channel when they are living it
    channel = member.guild.system_channel
    print(time.strftime("%H:%M:%S UTC ",time.gmtime()) + f'{member} se ha ido del discord server ({member.guild.name}).')
    await channel.send(f'Un miembro ({member})ha dejado el canal!!')

#Update Users
@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    #game = [i for i in after.activity if str(i.type)=='playing']
    #if game:
    #    print(game[0].name)
    print(f'Miembro actualizado: {after.name} {after.activities}')
    print("pending before: " , before.pending)
    print("pending after: ", after.pending)

#Timing of Messages & Joins
@tasks.loop()
async def update_stats():
    await bot.wait_until_ready()
    global messages, joined

    while not bot.is_closed():
        try:
            with open("stats.txt", "a") as filestat:
                filestat.write(f"{time.strftime("%H:%M:%S UTC ",time.gmtime())}, Messages: {messages}, Member Joined: {joined}\n") 
            messages=0
            joined=0

            await asyncio.sleep(900)
        except Exception as e:
            print(e)
            await asyncio.sleep(900)


#ERRORs
@bot.event
async def on_error(event, *args, **kwargs):
    """
    Catches any exception that occurs during the bot's loop.
    If any exception is raised in ``on_error``, it will `not` be handled.

    The exception itself can be accessed from :class:`sys.exc_info`.

    Args:
        event:
            The name of the event that raised the exception.

        *args:
            The positional arguments for the event that raised the exception

        **kwargs:
             The keyword arguments for the event that raised the exception.

    """
    print(time.strftime("%H:%M:%S UTC ",time.gmtime()) + "OH NO!, AN ERROR ;(")
    print(time.strftime("%H:%M:%S UTC ",time.gmtime()) + "Error from:", event)
    print(time.strftime("%H:%M:%S UTC ",time.gmtime()) + "Error context:", args, kwargs)

    from sys import exc_info

    exc_type, value, traceback = exc_info()
    print("Exception type:", exc_type)
    print("Exception value:", value)
    print("Exception traceback object:", traceback)

    with open('error.log', 'a') as log:
        log.write(f'Unhandled message: {args[0]}\n')
        log.close()

#COMMANDS errors
@bot.event
async def on_command_error(ctx : commands.Context, error: commands.CommandError ):
    if isinstance (error, commands.CommandNotFound):
        await ctx.send('Command not Found.')

    if isinstance (error, commands.MissingRequiredArgument):
        await ctx.send('You do not have write the correct command. Missing Argument')
    
    if isinstance (error, commands.MissingPermissions):
        await ctx.send('You do not have permissions on this command. Missing Permissions')


#Command to get Server information
@bot.command(name='bcrinfo')
async def discordInfo(ctx):
    #Get server information

    print ("Server information: " + ctx.guild.name)
    """
    for guild in bot.guilds:
        print(f'Discord Server Name: {guild.name} -> (id Discord Server: {guild.id})')
        guild_count = guild_count + 1


    own = guild.owner._user
    tim= str(guild.created_at)
    txt_channels = str(guild.text_channels)
    vioce_channels = str(guild.voice_channels)
    embeds= discord.Embed(
        timestamp=ctx.message.created_at,
        title='Server Information',
        color=0xFF0000)
    embeds.add_field(name='Name', value=f'{ctx.guild}')
    embeds.add_field(name='Owner', value=f'{own.mention}')
    embeds.add_field(name='Created:', value=f'{tim}')
    embeds.add_field(name='Members', value=f'{ctx.guild.member_count}')
    embeds.add_field(name='Text Channels', value=f'{txt_channels}')
    embeds.add_field(name='Voice channels', value=f'{vioce_channels}')
    
    await ctx.channel.send(embed=embeds)
    """

#Command para consulta el "clima"
@bot.command(name='clima')
async def weather(ctx, code):
        city = str(ctx.message.content[slice(7,len(ctx.message.content))])
        city = city.replace(' ','%20')
        """
        print ('city :', city)
        print ('len :', len(ctx.message.content))
        print ('slice:' , slice(5,len(ctx.message.content)))
        print ('CTX Message Content:' , ctx.message.content[slice(7,len(ctx.message.content))])
        print ('City: ', city)
        """
        result = get_weather(city)
        
        await ctx.channel.send(embed=result)

        
# Funcion Get Weather with City parameter on URL string. In this case we use the site API.WEATHERAPI.COM with a free account.
def get_weather(city):
    try:
        WEATHERAPIKEY = os.getenv('WEATHERAPIKEY')
        base_url ="https://api.weatherapi.com/v1/current.json?key=" + WEATHERAPIKEY  #"I am using api from https://www.weatherapi.com"
        complete_url = base_url + "&q=" + city + "&lang=es" 
        print('Complete URL ' + complete_url)
        response = requests.get(complete_url)

        if response.status_code==200:
            result = response.json()

            city = result['location']['name']
            country = result['location']['country']
            time = result['location']['localtime']
            wcond = result['current']['condition']['text']
            celcius = result['current']['temp_c']
            fclike = result['current']['feelslike_c']
            last_updated = result['current']['last_updated']
            icon = result['current']['condition']['icon']

            embed=discord.Embed(title=f"{city}"' Weather', description=f"{country}", colour=0x14aaeb)
            embed.add_field(name="Temperatura C°", value=f"{celcius}", inline=True)
            embed.add_field(name="Condiciones Viento", value=f"{wcond}", inline=True)
            embed.add_field(name="Sensacion Termica C°", value=f"{fclike}", inline=True)
            embed.add_field(name="Ultima Update", value=f"{last_updated}", inline=True)
            embed.set_thumbnail(url=f"https:{icon}")
            embed.set_footer(text="Hora : "f"{time}")
            return embed
        elif response.status_code == 404:
            embed=discord.Embed(title='Busqueda NO encontrada', colour=0x14aaeb)
            embed.add_field(name="Error", value="Oops!!! Please enter a right city name", inline=True)
            embed.add_field(name="Example", value="Example: !clima London", inline=True)
            return embed
        elif response.status_code == 500:
            embed=discord.Embed(title='Error API (500)', colour=0x14aaeb)
            embed.add_field(name="Error", value="Oops!!! Servicio caido", inline=True)
            return embed
        elif response.status_code == 503:
            embed=discord.Embed(title='Servicio NO Disponible (503)', colour=0x14aaeb)
            embed.add_field(name="Error", value="Oops!!! Servicio caido", inline=True)
            return embed
    except:
        embed=discord.Embed(title='Sin respuesta/error', colour=0x14aaeb)
        embed.add_field(name="Error", value=f"Oops!!! HTML code : {response.status_code}", inline=True)
        return embed

#Loop to count users and SAVE into log.txt
links= ['discord.gg/TNxdAV9S']
@tasks.loop(minutes=15)
async def inviting():
    invites = [await bot.fetch_invite(i,with_counts=True) for i in links] #Invite Objets
    counts =[getattr(i,'approximate_presence_count') for i in invites] #Presence Counts

    print(datetime.datetime.today().strftime("%d/%m/%y, %H:%M:%S ")+f' Presencia activa : {str(counts)}')
    with open('log.txt', 'a') as file:
        file.write(datetime.datetime.today().strftime("%D/%M/%Y, %H:%M:%S ")+ ','.join(map(str,counts))+'\n')


#Command connected-users
@bot.command(name='connected-users')
async def online_users(ctx):
    print ('command connected-users is running................................ ->')
    online_m, offline_m = [],[]
    #Loop over each member in guild.members
    for m in ctx.guild.members:
        #add to list of online members (online_m) if status is online/dnd, else add to offline_m
        (online_m if str(m.status) in ("online","dnd") else offline_m).append(str(m))
    await ctx.send (f"Online -> {', '.join(online_m)}\nOffline -> {', '.join(offline_m)} ")

    #Declaro lista vacia y columnas de la lista
    list_users = []
    users_columns = ['member_id','name','display_name','joined_at','server_name','server_id','activities']

    #Get members of this Guild
    for member in ctx.guild.members:
        #if not member.bot:
        activity = member.activities
        activitylist = list(activity)
        print(f'Activities: {member.activity}')
        to_add_member = [str(member.id),member.name,str(member.display_name),member.joined_at,ctx.guild.name,ctx.guild.id,member.activities]
        list_users.append (to_add_member)
    #Create a Dataframe of Members
    df_users = pd.DataFrame(list_users,columns=users_columns)
    print(df_users)

    #Print Games
    print ('--------------------------------------------------------------------------------------')
    for member in ctx.guild.members:
        #for activity in member.activities:
        print(f' Member: {member.name} | Activity: {member.activity} | Status: {member.status} | Server: {ctx.guild.name} ({ctx.guild.id})')
        await ctx.send (f' Member:{member.name} | Activity: {member.activity} | Status: {member.status}')
    print ('--------------------------------------------------------------------------------------')
    print ('command connected-users ending................................ <-')


#Command to Stop the bot
@bot.command(name='close')
async def close(ctx):
    embeder = discord.Embed(
            title = f'Bot status name: -> {bot.user.name}',
            description = 'The discord bot is offline.',
            colour = discord.Colour.red()
        )
    embeder.set_footer(text='Bot offline')
    await ctx.send(embed=embeder)
    await bot.close()



#Command to help the bot
@bot.command(name='helper')
async def help(ctx):
    #Help Bot

    embedh = discord.Embed(
        title = f'Help on Bot:-> {bot.user.name}',
        description = 'Some useful commands',
        colour = discord.Colour.blue()
    )
    #embedh.set_thumbnail(url=f'{botAvatar}')
    #embedh.set_image(url=f'{botAvatar}')
    embedh.add_field(name="hola (hello)",value="Greets the user", inline=False)
    embedh.add_field(name="!clima NY",value="Give the weather on ONE city o country", inline=False)
    embedh.add_field(name="!connected-users",value="Information of Users", inline=False)
    embedh.set_footer(text='helping to use bot commands')
    await ctx.send(content=None,embed=embedh)


bot.run(TOKEN)