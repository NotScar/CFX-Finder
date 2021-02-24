from classes import cfxBot
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="'")
cfxBot = cfxBot()

@bot.event
async def on_ready():
    print("Ready!")
    await bot.change_presence(activity=discord.Game('scar#6666 to buy 🔥'))

@bot.command()
async def cfx(ctx, code: str):
    if not (isinstance(ctx.channel, discord.channel.DMChannel)):
        if cfxBot.whitelistCheck(ctx.message.author.id,'subscriber') == True:
            cfxInformation = cfxBot.cfxInformation(code)
            if cfxInformation == 'Error':
                await ctx.send(embed = cfxBot.createEmbed('Address may be invalid. Retry',{}))
            else:
                await ctx.send(embed = cfxBot.createEmbed('',{
                    0: {'name':'NAME','content': cfxInformation['Name']},
                    1: {'name':'IP','content': cfxInformation['IP']},
                    2: {'name':'PORT','content':cfxInformation['Port']},
                    3: {'name':'HOSTING','content':cfxInformation['ISP']},
                    4: {'name':'LOCATION','content':cfxInformation['Location']}
                    }))

@bot.command()
async def status(ctx):
    if not (isinstance(ctx.channel, discord.channel.DMChannel)):
        statusExp = cfxBot.getExpiration(ctx.message.author.id)
        if not (statusExp == False):
            await ctx.send(embed = cfxBot.createEmbed('Your subscription will expire on %s' % statusExp,{}))

@bot.command()
async def add(ctx, userid: int, expiration: str):
    if not (isinstance(ctx.channel, discord.channel.DMChannel)):
        if cfxBot.whitelistCheck(ctx.message.author.id,'admin') == True and not (userid == None and expiration == None):
            cfxBot.addUser(userid,expiration)
            await ctx.send(embed = cfxBot.createEmbed('Added %d to whitelist with expiration on %s' % (userid,expiration),{}))


@bot.command()
async def remove(ctx, userid: int):
    if not (isinstance(ctx.channel, discord.channel.DMChannel)):
        if cfxBot.whitelistCheck(ctx.message.author.id,'admin') == True and not (userid == None):
            cfxBot.removeUser(userid)
            await ctx.send(embed = cfxBot.createEmbed('Removed %d from whitelist' % userid,{}))

@bot.command()
async def iplookup(ctx, ip: str):
    if not (isinstance(ctx.channel, discord.channel.DMChannel)):
        lookupResult = cfxBot.lookupIp(ip)
        if not (lookupResult == False):
            await ctx.send(embed = cfxBot.createEmbed('',{
                    0: {'name':'IP','content': lookupResult['query']},
                    1: {'name':'ISP','content': lookupResult['isp']},
                    2: {'name':'Country','content': lookupResult['country']},
                    3: {'name':'Region','content': lookupResult['regionName']},
                    4: {'name':'City','content': lookupResult['city']},
                    5: {'name':'ZIP','content': lookupResult['zip']},
                    6: {'name':'ASN','content': lookupResult['as']},
                    }))
        


bot.run("")