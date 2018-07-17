import aiohttp
from discord.ext import commands
import discord
import asyncio
import requests
f = open('token.txt')
token = f.read()
f.close()
bot = commands.Bot(command_prefix='!')

async def checkloop():
    while True:
        await asyncio.sleep(5)
        filevar = open('users.txt')
        filevarread = filevar.readlines()
        for i in filevarread:
            filevarread[filevarread.index(i)] = filevarread[filevarread.index(i)].replace('\n', '')
        filevar.close()
        discordlist = []
        owlist = []
        a = iter(filevarread)
        userlist = list(zip(a,a,a))
        for i in userlist:
            r = requests.get('http://ow-api.herokuapp.com/profile/pc/us/' + i[1])
            if bot.get_server(i[2]).get_member(i[0]).nick == None:
                oldnick = bot.get_server(i[2]).get_member(i[0]).name.split(' SR: ', 1)[0]
            else:
                oldnick = bot.get_server(i[2]).get_member(i[0]).nick.split(' SR: ', 1)[0]
            await bot.change_nickname(bot.get_server(i[2]).get_member(i[0]), oldnick + ' SR: ' + str(r.json()['competitive']['rank']))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.loop.create_task(checkloop())

@bot.command(pass_context=True)
async def start(ctx, user):
    user = user.replace('#','-')
    r = requests.get('http://ow-api.herokuapp.com/profile/pc/us/' + user)
    owstats = r.json()
    if owstats == {}:
        await bot.say('Error: account not found.')
        return
    if r.json()['competitive']['rank'] > 4000:
        await bot.say('get fuckin baited, i know youre trying to cheat')
        return

    f = open('users.txt', 'r')
    fileread = f.read()
    f.seek(0)
    filereadlines = f.readlines()
    f.close()
    for i in filereadlines:
        if i == ctx.message.author.id:
            await bot.say('dont say start twice')
            return
    f = open('users.txt', 'w')
    if fileread == '':
        f.write(fileread + ctx.message.author.id + '\n' + user + '\n' + ctx.message.server.id)
    else:
        f.write(fileread + '\n' + ctx.message.author.id + '\n' + user + '\n' + ctx.message.server.id)
    f.close()


bot.run(token)
