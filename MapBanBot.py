import discord

print(discord.__version__)
intents = discord.Intents.default()
intents.members = True
intents.presences = True
from csclass import cs
from r6class import r6
from valclass import valorant
from discord.ext import commands
from discord.utils import get
import shutil
import random
import asyncio


BOT_PREFIX = "?"

getToken = open("../discordtoken.txt", "r")

TOKEN = getToken.readline().strip()

#=============Ban list==================
CSBANS = []
R6BANS = []
VALBANS = []
#=======================================





client = commands.Bot(command_prefix=BOT_PREFIX, intents = intents)
client.remove_command('help')

#=============Channels=================
client.R6channel = 721312912630611968
client.CSchannel = 721312912630611968
client.VALchannel = 732600159669846127  
client.TESTchannel = 717009987066527845
#=======================================
client.TestMode = False

@client.command(pass_context=True)
async def help(ctx):
    message = "**Commands: \n?startcsbans\n?startr6bans\n?help\n**"
    message += "NOTE: If your target user has a space or special characters in their name, put "" when typing their name.\n\n"
    message += "**Usage:**\n?start__bans USER 1/3\nExample: For a cs bo3, ?startcsbans Stosh 3. For a r6 bo1, ?startr6bans Stosh 1\n"
    message += "Message Stosh on discord if you have any problems :)\n"
    #await client.send_message(ctx.message.author, message)
    await ctx.message.author.send(message)

@client.command(pass_context=True)
async def setTestMode(ctx):
    client.R6channel = client.TESTchannel
    client.CSchannel = client.TESTchannel
    client.VALchannel = client.TESTchannel
    client.TestMode = True

@client.command(pass_context=True)
async def setNormalMode(ctx):
    client.R6channel = 721312912630611968
    client.CSchannel = 721312912630611968
    client.VALchannel = 732600159669846127  
    client.TestMode = False

@client.command(pass_context=True)
async def CheckMode(ctx):
    if client.TestMode == True:
        #await client.send_message(ctx.message.author, "Test mode enabled")
        await ctx.message.author.send("Test mode enabled")
    elif client.TestMode == False:
        #await client.send_message(ctx.message.author, "Test mode disabled")
        await ctx.message.author.send("Test mode disabled")


@client.command(pass_context=True)
async def test(ctx, user2):
    user2 = user2.replace("#", " ")
    print(user2)
    user2ID = ""

    for server in client.guilds:
        for channel in server.channels:
            if int(channel.id) == 717009987066527845:
                textchannel = channel    
    for server in client.guilds:
        for members in server.members:
            if members.name == user2:
                print("FOUND MEMBER " + members.name)
                #await client.send_message(textchannel, "Found member")    
                await textchannel.send("Found member")            
                user2ID = members.id
                member = members
                break
            if members.display_name == user2:
                print("FOUND MEMBER " + members.name)
                #await client.send_message(textchannel, "Found member")   
                await textchannel.send("Found member")               
                user2ID = members.id
                break                       


@client.command(pass_context=True)
async def startr6bans(ctx, user2, bestof):
    def checkAuthor(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    def checkMember(reaction, user):
            return user == member and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    user2 = user2.replace("#", " ")
    print(user2)
    user2ID = ""
    for server in client.guilds:
        for members in server.members:
            if members.name == user2:
                print("FOUND MEMBER " + members.name)
                user2ID = members.id
                break
            if members.display_name == user2:
                print("FOUND MEMBER " + members.name)
                user2ID = members.id
                break                  

    member = get(client.get_all_members(), id=user2ID)
    if member.id:
        print("member found")
        newr6bans = r6(1, str(ctx.message.author.name), str(user2), int(bestof))
        newr6bans.setUID(1, ctx.message.author.id)
        newr6bans.setUID(2, member.id)
        R6BANS.append(newr6bans)
        msg = newr6bans.startbans()
        #await client.send_message(ctx.message.author, msg)
        #await client.send_message(member, msg)
        await ctx.message.author.send(msg)
        await member.send(msg)
        if newr6bans.getBestof() == 1:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
            while newr6bans.checkMaps() > 1:
    
                print(newr6bans.getnextBan(), member.name)
                if newr6bans.getnextBan() == ctx.message.author.id:
                    msg = newr6bans.processBan()
                    #sent = await client.send_message(ctx.message.author, msg)
                    sent = await ctx.message.author.send(msg)
                    i = 0
                    for x, y in newr6bans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            #await client.add_reaction(sent, emoji)
                            await sent.add_reaction(emoji)
                            i += 1
                    #reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'], message=sent,
                    #check=lambda reaction, user: user == ctx.message.author)

                    reaction, user = await client.wait_for('reaction_add', check = checkAuthor)
                    msg = newr6bans.banpick(reaction2.index(reaction.emoji))
                    await ctx.message.author.send(msg)
                    #await client.send_message(ctx.message.author, msg)
                    await member.send(msg)
                    #await client.send_message(member, msg)
                elif newr6bans.getnextBan() == member.id:                    
                    msg = newr6bans.processBan()
                    #sent = await client.send_message(member, msg)
                    sent = await member.send(msg)
                    i = 0
                    for x, y in newr6bans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            #await client.add_reaction(sent, emoji)
                            await sent.add_reaction(emoji)
                            i += 1
                    #reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'], message=sent,
                    #check=lambda reaction, user: user == member)
                    #reaction, user = await client.wait_for('reaction_add')
                    reaction, user = await client.wait_for('reaction_add', check = checkMember)
                    print(reaction.emoji)
                    msg = newr6bans.banpick(reaction2.index(reaction.emoji))
                    await ctx.message.author.send(msg)
                    await member.send(msg)
                    #await client.send_message(ctx.message.author, msg)
                    #await client.send_message(member, msg)                        
            #await client.send_message(ctx.message.author, newr6bans.getRemainingMaps())
            #await client.send_message(member, newr6bans.getRemainingMaps())
            await ctx.message.author.send(newr6bans.getRemainingMaps())
            await member.send(newr6bans.getRemainingMaps())
            for server in client.guilds:
                for channel in server.channels:
                    if int(channel.id) == client.R6channel:
                        textchannel = channel
            #await client.send_message(textchannel, newr6bans.getHistory())
            #await client.send_message(textchannel, newr6bans.getRemainingMaps())
            await textchannel.send(newr6bans.getHistory())
            await textchannel.send(newr6bans.getRemainingMaps())

        if newr6bans.getBestof() == 3:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
            while newr6bans.checkMaps() >= 2:
              
                print(newr6bans.getnextBan(), member.name)
                if newr6bans.getnextBan() == ctx.message.author.id:
                    msg = newr6bans.processBan()
                    #sent = await client.send_message(ctx.message.author, msg)
                    sent = await ctx.message.author.send(msg)
                    i = 0
                    for x, y in newr6bans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            #await client.add_reaction(sent, emoji)
                            await sent.add_reaction(emoji)
                            i += 1
                    #reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'], message=sent,
                    #check=lambda reaction, user: user == ctx.message.author)
                    reaction, user = await client.wait_for('reaction_add', check = checkAuthor)
                    msg = newr6bans.banpick(reaction2.index(reaction.emoji))
                    #await client.send_message(ctx.message.author, msg)
                    #await client.send_message(member, msg)  
                    await ctx.message.author.send(msg)
                    await member.send(msg)   
                elif newr6bans.getnextBan() == member.id:
                    msg = newr6bans.processBan()
                    #sent = await client.send_message(member, msg)
                    sent = await member.send(msg)
                    i = 0
                    for x, y in newr6bans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            #await client.add_reaction(sent, emoji)
                            await sent.add_reaction(emoji)
                            i += 1
                    #reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'], message=sent,
                    #check=lambda reaction, user: user == member)
                    reaction, user = await client.wait_for('reaction_add', check = checkMember)
                    msg = newr6bans.banpick(reaction2.index(reaction.emoji))
                    #await client.send_message(ctx.message.author, msg)
                    #await client.send_message(member, msg)   
                    await ctx.message.author.send(msg)
                    await member.send(msg)  
            #await client.send_message(ctx.message.author, newr6bans.getRemainingMaps())
            #await client.send_message(member, newr6bans.getRemainingMaps()) 
            await ctx.message.author.send(newr6bans.getRemainingMaps())  
            await member.send(newr6bans.getRemainingMaps())               
            for server in client.guilds:
                for channel in server.channels:
                    if int(channel.id) == client.R6channel:
                        textchannel = channel
            #await client.send_message(textchannel, newr6bans.getHistory())
            #await client.send_message(textchannel, newr6bans.getRemainingMaps()) 
            await textchannel.send(newr6bans.getHistory())   
            await textchannel.send(newr6bans.getRemainingMaps())     

    else:
        print("member not found")
        #await client.send_message(ctx.message.author, "The discord user you inputted cannot be found.")
        await ctx.message.author.send("The discord user you inputted cannot be found.")

@client.command(pass_context=True)
async def startvalbans(ctx, user1, user2, bestof):
    def checkAuthor(reaction, user):
            return user == team1 and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    def checkMember(reaction, user):
            return user == team2 and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']    
    user1 = user1.replace("#", " ")   
    user2 = user2.replace("#", " ")
    print(user1)
    print(user2)
    user2ID = ""
    user1ID = ""
    for server in client.guilds:
        for members in server.members:
            if members.name == user1:
                print("FOUND MEMBER " + members.name)
                user1ID = members.id
                break
            if members.display_name == user1:
                print("FOUND MEMBER " + members.name)
                user1ID = members.id  
                break       
    for server in client.guilds:
        for members in server.members:
            if members.name == user2:
                print("FOUND MEMBER " + members.name)
                user2ID = members.id
                break
            if members.display_name == user2:
                print("FOUND MEMBER " + members.name)
                user2ID = members.id  
                break
    team1 = get(client.get_all_members(), id=user1ID)            
    team2 = get(client.get_all_members(), id=user2ID)
    if team1.id and team2.id:
        print("members found")
        newvalbans = valorant(1, str(user1), str(user2), int(bestof))
        newvalbans.setUID(1, team1.id)
        newvalbans.setUID(2, team2.id)
        VALBANS.append(newvalbans)
        msg = newvalbans.startbans()
        #await client.send_message(ctx.message.author, msg)
        #await client.send_message(team1, msg)
        #await client.send_message(team2, msg)
        #await ctx.message.author.send(msg)
        await team1.send(msg)
        await team2.send(msg)
        if newvalbans.getBestof() == 1:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
            while newvalbans.checkMaps() > 2:
    
                #print(newvalbans.getnextBan(), team1.name)
                if newvalbans.getnextBan() == team1.id:
                    msg = newvalbans.processBan()
                    #sent = await client.send_message(team1, msg)
                    sent = await team1.send(msg)
                    i = 0
                    for x, y in newvalbans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            #await client.add_reaction(sent, emoji)
                            await sent.add_reaction(emoji)
                            i += 1
                    #reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'], message=sent,
                    #check=lambda reaction, user: user == team1)
                    reaction, user = await client.wait_for('reaction_add', check = checkAuthor)
                    msg = newvalbans.banpick(reaction2.index(reaction.emoji))
                    #await client.send_message(team1, msg)
                    #await client.send_message(team2, msg)
                    await team1.send(msg)
                    await team2.send(msg)
                elif newvalbans.getnextBan() == team2.id:                    
                    msg = newvalbans.processBan()
                    #sent = await client.send_message(team2, msg)
                    sent = await team2.send(msg)
                    i = 0
                    for x, y in newvalbans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            #await client.add_reaction(sent, emoji)
                            await sent.add_reaction(emoji)
                            i += 1
                    #reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'], message=sent,
                    #check=lambda reaction, user: user == team2)
                    reaction, user = await client.wait_for('reaction_add', check = checkMember)
                    msg = newvalbans.banpick(reaction2.index(reaction.emoji))
                    #await client.send_message(team1, msg)
                    #await client.send_message(team2, msg)
                    await team1.send(msg)
                    await team2.send(msg)
            newvalbans.randBan()
            #await client.send_message(team1, newvalbans.getRemainingMaps())
            #await client.send_message(team2, newvalbans.getRemainingMaps())
            await team1.send(newvalbans.getRemainingMaps())
            await team2.send(newvalbans.getRemainingMaps())            
            for server in client.guilds:
                for channel in server.channels:
                    if int(channel.id) == client.VALchannel: #717009987066527845: 732600159669846127:
                        textchannel = channel
            #await client.send_message(textchannel, newvalbans.getHistory())
            #await client.send_message(textchannel, newvalbans.getRemainingMaps())
            await textchannel.send(newvalbans.getHistory())
            await textchannel.send(newvalbans.getRemainingMaps())

        if newvalbans.getBestof() == 3:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
            while newvalbans.checkMaps() >= 2:
              
                #print(newvalbans.getnextBan(), member.name)
                if newvalbans.getnextBan() == team1.id:
                    msg = newvalbans.processBan()
                    #sent = await client.send_message(ctx.message.author, msg)
                    sent = await team1.send(msg)
                    i = 0
                    for x, y in newvalbans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            #await client.add_reaction(sent, emoji)
                            await sent.add_reaction(emoji)
                            i += 1
                    #reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'], message=sent,
                    #check=lambda reaction, user: user == ctx.message.author)
                    reaction, user = await client.wait_for('reaction_add', check = checkAuthor)                    
                    msg = newvalbans.banpick(reaction2.index(reaction.emoji))
                    #await client.send_message(ctx.message.author, msg)
                    #await client.send_message(member, msg)     
                    await team1.send(msg)
                    await team2.send(msg)
                elif newvalbans.getnextBan() == team2.id:
                    msg = newvalbans.processBan()
                    #sent = await client.send_message(member, msg)
                    sent = await team2.send(msg)
                    i = 0
                    for x, y in newvalbans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            #await client.add_reaction(sent, emoji)
                            await sent.add_reaction(emoji)
                            i += 1
                    #reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'], message=sent,
                    #check=lambda reaction, user: user == member)
                    reaction, user = await client.wait_for('reaction_add', check = checkMember)                    
                    msg = newvalbans.banpick(reaction2.index(reaction.emoji))
                    #await client.send_message(ctx.message.author, msg)
                    #await client.send_message(member, msg)  
                    await team1.send(msg)
                    await team2.send(msg)   
            #await client.send_message(ctx.message.author, newvalbans.getRemainingMaps())
            #await client.send_message(member, newvalbans.getRemainingMaps())
            await team1.send(newvalbans.getRemainingMaps())    
            await team2.send(newvalbans.getRemainingMaps())
            for server in client.guilds:
                for channel in server.channels:
                    if int(channel.id) == client.VALchannel:
                        textchannel = channel
            #await client.send_message(textchannel, newvalbans.getHistory())
            #await client.send_message(textchannel, newvalbans.getRemainingMaps()) 
            await textchannel.send(newvalbans.getHistory())        
            await textchannel.send(newvalbans.getRemainingMaps())

    else:
        print("member not found")
        #await client.send_message(ctx.message.author, "The discord user you inputted cannot be found.")
        await ctx.message.author.send("The discord user you inputted cannot be found.")

@client.command(pass_context=True)
async def startcsbans(ctx, user2, bestof):
    def checkAuthor(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']

    def checkMember(reaction, user):
            return user == member and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']

    user2 = user2.replace("#", " ")
    print(user2)
    user2ID = ""
    for server in client.guilds:
        for members in server.members:
            if members.name == user2:
                print("FOUND MEMBER " + members.name)
                user2ID = members.id
                break
            if members.display_name == user2:
                print("FOUND MEMBER " + members.name)
                user2ID = members.id  
                break

    member = get(client.get_all_members(), id=user2ID)
    if member.id:
        print("member found")
        newcsbans = cs(1, str(ctx.message.author.name), str(user2), int(bestof))
        newcsbans.setUID(1, ctx.message.author.id)
        newcsbans.setUID(2, member.id)
        CSBANS.append(newcsbans)
        msg = newcsbans.startbans()
        #await client.send_message(ctx.message.author, msg)
        #await client.send_message(member, msg)
        await ctx.message.author.send(msg)
        await member.send(msg)
        if newcsbans.getBestof() == 1:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
            while newcsbans.checkMaps() > 1:
    
                print(newcsbans.getnextBan(), member.name)
                if newcsbans.getnextBan() == ctx.message.author.id:
                    msg = newcsbans.processBan()
                    #sent = await client.send_message(ctx.message.author, msg)
                    sent = await ctx.message.author.send(msg)
                    i = 0
                    for x, y in newcsbans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            #await client.add_reaction(sent, emoji)
                            await sent.add_reaction(emoji)
                            i += 1
                    #reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'], message=sent,
                    #check=lambda reaction, user: user == ctx.message.author)
                    
                    reaction, user = await client.wait_for('reaction_add', check = checkAuthor)
                    msg = newcsbans.banpick(reaction2.index(reaction.emoji))
                    #await client.send_message(ctx.message.author, msg)
                    await ctx.message.author.send(msg)
                    #await client.send_message(member, msg)
                    await member.send(msg)
                elif newcsbans.getnextBan() == member.id:                    
                    msg = newcsbans.processBan()
                    #sent = await client.send_message(member, msg)
                    sent = await member.send(msg)
                    i = 0
                    for x, y in newcsbans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            #await client.add_reaction(sent, emoji)
                            await sent.add_reaction(emoji)
                            i += 1
                    #reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'], message=sent,
                    #check=lambda reaction, user: user == member)
                    reaction, user = await client.wait_for('reaction_add', check = checkMember)
                    msg = newcsbans.banpick(reaction2.index(reaction.emoji))
                    #await client.send_message(ctx.message.author, msg)
                    #await client.send_message(member, msg)    
                    await ctx.message.author.send(msg)
                    await member.send(msg)                    
            #await client.send_message(ctx.message.author, newcsbans.getRemainingMaps())
            #await client.send_message(member, newcsbans.getRemainingMaps())
            await ctx.message.author.send(newcsbans.getRemainingMaps())
            await member.send(newcsbans.getRemainingMaps())
            for server in client.guilds:
                for channel in server.channels:
                    if int(channel.id) == client.CSchannel: #717009987066527845: #721312912630611968
                        textchannel = channel
            #await client.send_message(textchannel, newcsbans.getHistory())
            #await client.send_message(textchannel, newcsbans.getRemainingMaps())
            await textchannel.send(newcsbans.getHistory())
            await textchannel.send(newcsbans.getRemainingMaps())

        if newcsbans.getBestof() == 3:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
            while newcsbans.checkMaps() >= 2:
              
                print(newcsbans.getnextBan(), member.name)
                if newcsbans.getnextBan() == ctx.message.author.id:
                    msg = newcsbans.processBan()
                    #sent = await client.send_message(ctx.message.author, msg)
                    sent = await ctx.message.author.send(msg)
                    i = 0
                    for x, y in newcsbans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            #await client.add_reaction(sent, emoji)
                            await sent.add_reaction(emoji)
                            i += 1
                    #reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'], message=sent,
                    #check=lambda reaction, user: user == ctx.message.author)
                    reaction, user = await client.wair_for('reaction_add', check = checkAuthor)
                    msg = newcsbans.banpick(reaction2.index(reaction.emoji))
                    #await client.send_message(ctx.message.author, msg)
                    #await client.send_message(member, msg)  
                    await ctx.message.author.send(msg)
                    await member.send(msg)   
                elif newcsbans.getnextBan() == member.id:
                    msg = newcsbans.processBan()
                    #sent = await client.send_message(member, msg)
                    sent = await member.send(msg)
                    i = 0
                    for x, y in newcsbans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            #await client.add_reaction(sent, emoji)
                            await sent.add_reaction(emoji)
                            i += 1
                    #reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'], message=sent,
                    #check=lambda reaction, user: user == member)
                    reaction, user = await client.wait_for('reaction_add', check = checkMember)
                    msg = newcsbans.banpick(reaction2.index(reaction.emoji))
                    #await client.send_message(ctx.message.author, msg)
                    #await client.send_message(member, msg)     
                    await ctx.message.author.send(msg)
                    await member.send(msg)
            #await client.send_message(ctx.message.author, newcsbans.getRemainingMaps())
            #await client.send_message(member, newcsbans.getRemainingMaps())    
            await ctx.message.author.send(msg)
            await member.send(msg)
            for server in client.guilds:
                for channel in server.channels:
                    if int(channel.id) == client.CSchannel: #717009987066527845: #721312912630611968
                        textchannel = channel
            #await client.send_message(textchannel, newcsbans.getHistory())
            #await client.send_message(textchannel, newcsbans.getRemainingMaps())       
            await textchannel.send(newcsbans.getHistory())
            await textchannel.send(newr6bans.getRemainingMaps())  

    else:
        print("member not found")
        #await client.send_message(ctx.message.author, "The discord user you inputted cannot be found.")
        await ctx.message.author.send("The discord user you inputted cannot be found.")
        
@client.command(pass_context=True)
async def close(ctx):
    print("Closing Bot")    
    exit()



client.run(TOKEN)  