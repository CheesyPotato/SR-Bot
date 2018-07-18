import aiohttp
from discord.ext import commands
import discord
import asyncio
import requests
f = open('token.txt')
token = f.read()
f.close()
bot = commands.Bot(command_prefix='::')

async def checkloop():
    while True:

        filevar = open('users.txt')
        filevarread = filevar.readlines()
        filevarcopy = filevarread.copy()
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
            if bot.get_server(i[2]).get_member(bot.user.id).server_permissions.manage_nicknames:
                await bot.change_nickname(bot.get_server(i[2]).get_member(i[0]), oldnick + ' SR: ' + str(r.json()['competitive']['rank']))
        await asyncio.sleep(5)
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='::help'))
    bot.loop.create_task(checkloop())

@bot.command(pass_context=True)
async def start(ctx, user=None):

    if user == None:
        await bot.say('Error: put your battletag after ::start')
        return
    if ctx.message.author.id == ctx.message.server.owner.id:
        await bot.say("Sorry, the bot can't change the owner's nickname :sob:")
        return
    user = user.replace('#','-')
    r = requests.get('http://ow-api.herokuapp.com/profile/pc/us/' + user)
    owstats = r.json()
    if owstats == {}:
        await bot.say('Error: account not found.')
        return

    f = open('users.txt', 'r')
    fileread = f.read()
    f.seek(0)
    filereadlines = f.readlines()
    f.close()
    a = iter(filereadlines)
    filereadlist = list(zip(a,a,a))
    print(filereadlist)
    for i in filereadlist:
        if i[0].replace('\n', '') == ctx.message.author.id and i[2].replace('\n', '') == ctx.message.server.id:
            await bot.say('Error: you have already registered in this server.')
            return
    f = open('users.txt', 'w')
    if fileread == '':
        f.write(fileread + ctx.message.author.id + '\n' + user + '\n' + ctx.message.server.id)
    else:
        f.write(fileread + '\n' + ctx.message.author.id + '\n' + user + '\n' + ctx.message.server.id)
    f.close()
    await bot.say('Success! updating...')
@bot.command(pass_context=True)
async def remove(ctx):
    f = open('users.txt', 'r')
    fileread = f.readlines()
    f.seek(0)
    f.close()
    a = iter(fileread)
    filereadlist = list(zip(a,a,a))
    for i in filereadlist:
        if i[0].replace('\n', '') == ctx.message.author.id and i[2].replace('\n', '') == ctx.message.server.id:
            filereadlist.remove(i)
            f = open('users.txt', 'w')
            f.writelines([i for sub in filereadlist for i in sub])
            f.close()
            await bot.say('Removed!')
            return
    await bot.say("You haven't registered yet in this server (::start <battletag>)")

bot.run(token)
#await bot.say('Error: not enough permissions (can the bot manage nicknames? is the member higher than the bot?)')
