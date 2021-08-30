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
client.R6channel = 855380291145039893
client.CSchannel = 855380291145039893
client.VALchannel = 855380291145039893 
client.TESTchannel = 717009987066527845
#=======================================
client.TestMode = False

@client.command(pass_context=True)
async def help(ctx):
    message = "**Commands: \n?startcsbans\n?startr6bans\n?help\n**"
    message += "NOTE: If your target user has a space or special characters in their name, put "" when typing their name.\n\n"
    message += "**Usage:**\n?start__bans USER 1/3\nExample: For a cs bo3, ?startcsbans Stosh 3. For a r6 bo1, ?startr6bans Stosh 1\n"
    message += "Message Stosh on discord if you have any problems :)\n"
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
        await ctx.message.author.send("Test mode enabled")
    elif client.TestMode == False:
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
                await textchannel.send("Found member")            
                user2ID = members.id
                member = members
                break
            if members.display_name == user2:
                print("FOUND MEMBER " + members.name)
                await textchannel.send("Found member")               
                user2ID = members.id
                break                       


@client.command(pass_context=True)
async def startr6bans(ctx, user1, user2, bestof):
    def checkTeam1(reaction, user):
            return user == team1 and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    def checkTeam2(reaction, user):
            return user == team2 and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    def findMember(member):
        sanitisedMember = member.replace("#", " ")
        for server in client.guilds:
            for members in server.members:
                if members.name == sanitisedMember:
                    print("FOUND MEMBER " + members.name)
                    return members.id
                if members.display_name == sanitisedMember:
                    print("FOUND MEMBER " + members.name)
                    return members.id

    user1ID = ctx.message.raw_mentions[0]
    user2ID = ctx.message.raw_mentions[1]              

    team1 = get(client.get_all_members(), id=user1ID)
    team2 = get(client.get_all_members(), id=user2ID)
    if team1.id and team2.id:
        print("member found")
        newr6bans = r6(1, str(user1), str(user2), int(bestof))
        newr6bans.setUID(1, team1.id)
        newr6bans.setUID(2, team2.id)
        R6BANS.append(newr6bans)
        msg = newr6bans.startbans()
        await team1.send(msg)
        await team2.send(msg)
        if newr6bans.getBestof() == 1:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
            while newr6bans.checkMaps() > 1:
                if newr6bans.getnextBan() == team1.id:
                    msg = newr6bans.processBan()
                    sent = await team1.send(msg)
                    i = 0
                    for x, y in newr6bans.getAllmaps().items():
                        if y == "neutral":
                            emoji = reaction2[i]
                            await sent.add_reaction(emoji)
                            i += 1
                    reaction, user = await client.wait_for('reaction_add', check = checkTeam1)
                    msg = newr6bans.banpick(reaction2.index(reaction.emoji))
                    await team1.send(msg)
                    await team2.send(msg)
                elif newr6bans.getnextBan() == team2.id:                    
                    msg = newr6bans.processBan()
                    sent = await team2.send(msg)
                    i = 0
                    for x, y in newr6bans.getAllmaps().items():
                        if y == "neutral":
                            emoji = reaction2[i]
                            await sent.add_reaction(emoji)
                            i += 1
                    reaction, user = await client.wait_for('reaction_add', check = checkTeam2)
                    print(reaction.emoji)
                    msg = newr6bans.banpick(reaction2.index(reaction.emoji))
                    await team1.send(msg)
                    await team2.send(msg)
            await team1.send(newr6bans.getRemainingMaps())
            await team2.send(newr6bans.getRemainingMaps())
            for server in client.guilds:
                for channel in server.channels:
                    if int(channel.id) == client.R6channel:
                        textchannel = channel
            await textchannel.send(newr6bans.getHistory())
            await textchannel.send(newr6bans.getRemainingMaps())

        if newr6bans.getBestof() == 3:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
            while newr6bans.checkMaps() >= 2:
              
                print(newr6bans.getnextBan(), team2.name)
                if newr6bans.getnextBan() == team1.id:
                    msg = newr6bans.processBan()
                    sent = await team1.send(msg)
                    i = 0
                    for x, y in newr6bans.getAllmaps().items():
                        if y == "neutral":
                            emoji = reaction2[i]
                            await sent.add_reaction(emoji)
                            i += 1
                    reaction, user = await client.wait_for('reaction_add', check = checkTeam1)
                    msg = newr6bans.banpick(reaction2.index(reaction.emoji))  
                    await team1.send(msg)
                    await team2.send(msg)   
                elif newr6bans.getnextBan() == team2.id:
                    msg = newr6bans.processBan()
                    sent = await team2.send(msg)
                    i = 0
                    for x, y in newr6bans.getAllmaps().items():
                        if y == "neutral":
                            emoji = reaction2[i]
                            await sent.add_reaction(emoji)
                            i += 1
                    reaction, user = await client.wait_for('reaction_add', check = checkTeam2)
                    msg = newr6bans.banpick(reaction2.index(reaction.emoji))
                    await team1.send(msg)
                    await team2.send(msg)  
            await team1.send(newr6bans.getRemainingMaps())  
            await team2.send(newr6bans.getRemainingMaps())               
            for server in client.guilds:
                for channel in server.channels:
                    if int(channel.id) == client.R6channel:
                        textchannel = channel
            await textchannel.send(newr6bans.getHistory())   
            await textchannel.send(newr6bans.getRemainingMaps())     

    else:
        print("member not found")
        await ctx.message.author.send("The discord user you inputted cannot be found.")

@client.command(pass_context=True)
async def startvalbans(ctx, user1, user2, bestof):
    #HELPER FUNCTIONS
    def checkAuthor(reaction, user):
            return user == team1 and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    def checkMember(reaction, user):
            return user == team2 and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']    
    #user1 = user1.replace("#", " ")   
    #user2 = user2.replace("#", " ")
    print(ctx.message.raw_mentions)
    #print(user1)
    #print(user2)
    user2ID = ctx.message.raw_mentions[1]
    user1ID = ctx.message.raw_mentions[0]
    #FIND MEMBERS
    """for server in client.guilds:
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
                break"""
    team1 = get(client.get_all_members(), id=user1ID)            
    team2 = get(client.get_all_members(), id=user2ID)
    #IF MEMBERS ARE FOUND
    if team1.id and team2.id:
        print("members found")
        newvalbans = valorant(1, str(user1), str(user2), int(bestof))
        newvalbans.setUID(1, team1.id)
        newvalbans.setUID(2, team2.id)
        VALBANS.append(newvalbans)
        msg = newvalbans.startbans()
        await team1.send(msg)
        await team2.send(msg)
        if newvalbans.getBestof() == 1:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
            while newvalbans.checkMaps() > 1:
                if newvalbans.getnextBan() == team1.id:
                    msg = newvalbans.processBan()
                    sent = await team1.send(msg)
                    i = 0
                    for x, y in newvalbans.getAllmaps().items():
                        if y == "neutral":
                            emoji = reaction2[i]
                            await sent.add_reaction(emoji)
                            i += 1
                    reaction, user = await client.wait_for('reaction_add', check = checkAuthor)
                    msg = newvalbans.banpick(reaction2.index(reaction.emoji))
                    await team1.send(msg)
                    await team2.send(msg)
                elif newvalbans.getnextBan() == team2.id:                    
                    msg = newvalbans.processBan()
                    sent = await team2.send(msg)
                    i = 0
                    for x, y in newvalbans.getAllmaps().items():
                        if y == "neutral":
                            emoji = reaction2[i]
                            await sent.add_reaction(emoji)
                            i += 1
                    reaction, user = await client.wait_for('reaction_add', check = checkMember)
                    msg = newvalbans.banpick(reaction2.index(reaction.emoji))
                    await team1.send(msg)
                    await team2.send(msg)
            #newvalbans.randBan()
            await team1.send(newvalbans.getRemainingMaps())
            await team2.send(newvalbans.getRemainingMaps())            
            for server in client.guilds:
                for channel in server.channels:
                    if int(channel.id) == client.VALchannel: #717009987066527845: 732600159669846127:
                        textchannel = channel
            await textchannel.send(newvalbans.getHistory())
            await textchannel.send(newvalbans.getRemainingMaps())

        if newvalbans.getBestof() == 3:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
            while newvalbans.checkMaps() > 2:
                if newvalbans.getnextBan() == team1.id:
                    msg = newvalbans.processBan()
                    sent = await team1.send(msg)
                    i = 0
                    for x, y in newvalbans.getAllmaps().items():
                        if y == "neutral":
                            emoji = reaction2[i]
                            await sent.add_reaction(emoji)
                            i += 1
                    reaction, user = await client.wait_for('reaction_add', check = checkAuthor)                    
                    msg = newvalbans.banpick(reaction2.index(reaction.emoji))   
                    await team1.send(msg)
                    await team2.send(msg)
                elif newvalbans.getnextBan() == team2.id:
                    msg = newvalbans.processBan()
                    sent = await team2.send(msg)
                    i = 0
                    for x, y in newvalbans.getAllmaps().items():
                        if y == "neutral":
                            emoji = reaction2[i]
                            await sent.add_reaction(emoji)
                            i += 1
                    reaction, user = await client.wait_for('reaction_add', check = checkMember)                    
                    msg = newvalbans.banpick(reaction2.index(reaction.emoji)) 
                    await team1.send(msg)
                    await team2.send(msg)
            newvalbans.randBan()   
            await team1.send(newvalbans.getRemainingMaps())    
            await team2.send(newvalbans.getRemainingMaps())
            for server in client.guilds:
                for channel in server.channels:
                    if int(channel.id) == client.VALchannel:
                        textchannel = channel
            await textchannel.send(newvalbans.getHistory())        
            await textchannel.send(newvalbans.getRemainingMaps())

    else:
        print("member not found")
        await ctx.message.author.send("The discord user you inputted cannot be found.")

@client.command(pass_context=True)
async def startcsbans(ctx, user1, user2, bestof):
    def checkAuthor(reaction, user):
            return user == team1 and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']

    def checkMember(reaction, user):
            return user == team2 and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']

    user1 = user1.replace("#", " ")
    print(user1)
    team1ID = ctx.message.raw_mentions[0]
    team2ID = ctx.message.raw_mentions[1]
    """for server in client.guilds:
        for members in server.members:
            if members.name == user1:
                print("FOUND MEMBER " + members.name)
                team1ID = members.id
                break
            if members.display_name == user1:
                print("FOUND MEMBER " + members.name)
                team1ID = members.id  
                break
    user2 = user2.replace("#", " ")
    print(user2)
    team2ID = ""
    for server in client.guilds:
        for members in server.members:
            if members.name == user2:
                print("FOUND MEMBER " + members.name)
                team2ID = members.id
                break
            if members.display_name == user2:
                print("FOUND MEMBER " + members.name)
                team2ID = members.id  
                break
"""
    team1 = get(client.get_all_members(), id=team1ID)
    team2 = get(client.get_all_members(), id=team2ID)
    if team1ID and team2ID:
        print("member found")
        newcsbans = cs(1, str(team1), str(team2), int(bestof))
        newcsbans.setUID(1, team1.id)
        newcsbans.setUID(2, team2.id)
        CSBANS.append(newcsbans)
        msg = newcsbans.startbans()
        await team1.send(msg)
        await team2.send(msg)
        if newcsbans.getBestof() == 1:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
            while newcsbans.checkMaps() > 1:
                print(newcsbans.getnextBan(), team2.name)
                if newcsbans.getnextBan() == team1.id:
                    msg = newcsbans.processBan()
                    sent = await team1.send(msg)
                    i = 0
                    for x, y in newcsbans.getAllmaps().items():
                        if y == "neutral":
                            emoji = reaction2[i]
                            await sent.add_reaction(emoji)
                            i += 1
                    
                    reaction, user = await client.wait_for('reaction_add', check = checkAuthor)
                    msg = newcsbans.banpick(reaction2.index(reaction.emoji))
                    await team1.send(msg)
                    await team2.send(msg)
                elif newcsbans.getnextBan() == team2.id:                    
                    msg = newcsbans.processBan()
                    sent = await team2.send(msg)
                    i = 0
                    for x, y in newcsbans.getAllmaps().items():
                        if y == "neutral":
                            emoji = reaction2[i]
                            await sent.add_reaction(emoji)
                            i += 1
                    reaction, user = await client.wait_for('reaction_add', check = checkMember)
                    msg = newcsbans.banpick(reaction2.index(reaction.emoji)) 
                    await team1.send(msg)
                    await team2.send(msg)                    
            await team1.send(newcsbans.getRemainingMaps())
            await team2.send(newcsbans.getRemainingMaps())
            for server in client.guilds:
                for channel in server.channels:
                    if int(channel.id) == client.CSchannel: #717009987066527845: #721312912630611968
                        textchannel = channel
            await textchannel.send(newcsbans.getHistory())
            await textchannel.send(newcsbans.getRemainingMaps())

        if newcsbans.getBestof() == 3:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
            while newcsbans.checkMaps() >= 2:
              
                print(newcsbans.getnextBan(), team2.name)
                if newcsbans.getnextBan() == team1.id:
                    msg = newcsbans.processBan()
                    sent = await team1.send(msg)
                    i = 0
                    for x, y in newcsbans.getAllmaps().items():
                        if y == "neutral":
                            emoji = reaction2[i]
                            await sent.add_reaction(emoji)
                            i += 1
                    reaction, user = await client.wait_for('reaction_add', check = checkAuthor)
                    msg = newcsbans.banpick(reaction2.index(reaction.emoji))
                    await team1.send(msg)
                    await team2.send(msg)   
                elif newcsbans.getnextBan() == team2.id:
                    msg = newcsbans.processBan()
                    sent = await team2.send(msg)
                    i = 0
                    for x, y in newcsbans.getAllmaps().items():
                        if y == "neutral":
                            emoji = reaction2[i]
                            await sent.add_reaction(emoji)
                            i += 1
                    reaction, user = await client.wait_for('reaction_add', check = checkMember)
                    msg = newcsbans.banpick(reaction2.index(reaction.emoji))  
                    await team1.send(msg)
                    await team2.send(msg)   
            await team1.send(msg)
            await team2.send(msg)
            for server in client.guilds:
                for channel in server.channels:
                    if int(channel.id) == client.CSchannel: #717009987066527845: #721312912630611968
                        textchannel = channel  
            await textchannel.send(newcsbans.getHistory())
            await textchannel.send(newcsbans.getRemainingMaps())  

    else:
        print("member not found")
        await team1.send("The discord user you inputted cannot be found.")
        
@client.command(pass_context=True)
async def close(ctx):
    print("Closing Bot")    
    exit()



client.run(TOKEN)  
