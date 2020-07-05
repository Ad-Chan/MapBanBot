import discord
from csclass import cs
from r6class import r6
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
#=======================================

#=============Variables=================
#csID = 0
#r6ID = 0
#=======================================


client = commands.Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

@client.command(pass_context=True)
async def help(ctx):
    message = "**Commands: \n?startcsbans\n?startr6bans\n?help\n**"
    message += "NOTE: If your target user has a space in their name, replace the space with a #.\n\n"
    message += "**Usage:**\n?start__bans USER 1/3\nExample: For a cs bo3, ?startcsbans Stosh 3. For a r6 bo1, ?startr6bans Stosh 1\n"
    message += "Message Stosh on discord if you have any problems :)\n"
    await client.send_message(ctx.message.author, message)

#@client.event
#async def on_react_add(reaction, user):
    
@client.command(pass_context=True)
async def test(ctx, user2):
    user2 = user2.replace("#", " ")
    print(user2)
    user2ID = ""
    for server in client.servers:
        for members in server.members:
            if members.name == user2:
                print("FOUND MEMBER " + members.name)
                user2ID = members.id
                break
            if members.display_name == user2:
                print("FOUND MEMBER " + members.name)
                user2ID = members.id
                break   

@client.command(pass_context=True)
async def startr6bans(ctx, user2, bestof):
    user2 = user2.replace("#", " ")
    print(user2)
    user2ID = ""
    for server in client.servers:
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
    if member:
        print("member found")
        newr6bans = r6(1, str(ctx.message.author.name), str(user2), int(bestof))
        R6BANS.append(newr6bans)
        msg = newr6bans.startbans()
        await client.send_message(ctx.message.author, msg)
        await client.send_message(member, msg)
        if newr6bans.getBestof() == 1:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
            while newr6bans.checkMaps() > 1:
    
                print(newr6bans.getnextBan(), member.name)
                if newr6bans.getnextBan() == ctx.message.author.name:
                    msg = newr6bans.processBan()
                    sent = await client.send_message(ctx.message.author, msg)
                    i = 0
                    for x, y in newr6bans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            await client.add_reaction(sent, emoji)
                            i += 1
                    reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'], message=sent,
                    check=lambda reaction, user: user == ctx.message.author)
                    msg = newr6bans.banpick(reaction2.index(reaction.reaction.emoji))
                    await client.send_message(ctx.message.author, msg)
                    await client.send_message(member, msg)
                elif str(newr6bans.getnextBan()) == str(member.name):                    
                    msg = newr6bans.processBan()
                    sent = await client.send_message(member, msg)
                    i = 0
                    for x, y in newr6bans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            await client.add_reaction(sent, emoji)
                            i += 1
                    reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'], message=sent,
                    check=lambda reaction, user: user == member)
                    msg = newr6bans.banpick(reaction2.index(reaction.reaction.emoji))
                    await client.send_message(ctx.message.author, msg)
                    await client.send_message(member, msg)                        
            await client.send_message(ctx.message.author, newr6bans.getRemainingMaps())
            await client.send_message(member, newr6bans.getRemainingMaps())
            for server in client.servers:
                for channel in server.channels:
                    if int(channel.id) == 721312912630611968:
                        textchannel = channel
            await client.send_message(textchannel, newr6bans.getHistory())
            await client.send_message(textchannel, newr6bans.getRemainingMaps())

        if newr6bans.getBestof() == 3:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
            while newr6bans.checkMaps() >= 2:
              
                print(newr6bans.getnextBan(), member.name)
                if newr6bans.getnextBan() == ctx.message.author.name:
                    msg = newr6bans.processBan()
                    sent = await client.send_message(ctx.message.author, msg)
                    i = 0
                    for x, y in newr6bans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            await client.add_reaction(sent, emoji)
                            i += 1
                    reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'], message=sent,
                    check=lambda reaction, user: user == ctx.message.author)
                    msg = newr6bans.banpick(reaction2.index(reaction.reaction.emoji))
                    await client.send_message(ctx.message.author, msg)
                    await client.send_message(member, msg)     
                elif str(newr6bans.getnextBan()) == str(member.name):
                    msg = newr6bans.processBan()
                    sent = await client.send_message(member, msg)
                    i = 0
                    for x, y in newr6bans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            await client.add_reaction(sent, emoji)
                            i += 1
                    reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'], message=sent,
                    check=lambda reaction, user: user == member)
                    msg = newr6bans.banpick(reaction2.index(reaction.reaction.emoji))
                    await client.send_message(ctx.message.author, msg)
                    await client.send_message(member, msg)     
            await client.send_message(ctx.message.author, newr6bans.getRemainingMaps())
            await client.send_message(member, newr6bans.getRemainingMaps())    
            for server in client.servers:
                for channel in server.channels:
                    if int(channel.id) == 721312912630611968:
                        textchannel = channel
            await client.send_message(textchannel, newr6bans.getHistory())
            await client.send_message(textchannel, newr6bans.getRemainingMaps())         

    else:
        print("member not found")
        await client.send_message(ctx.message.author, "The discord user you inputted cannot be found.")

@client.command(pass_context=True)
async def startcsbans(ctx, user2, bestof):
    user2 = user2.replace("#", " ")
    print(user2)
    user2ID = ""
    for server in client.servers:
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
    if member:
        print("member found")
        newcsbans = cs(1, str(ctx.message.author.name), str(user2), int(bestof))
        CSBANS.append(newcsbans)
        msg = newcsbans.startbans()
        await client.send_message(ctx.message.author, msg)
        await client.send_message(member, msg)
        if newcsbans.getBestof() == 1:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
            while newcsbans.checkMaps() > 1:
    
                print(newcsbans.getnextBan(), member.name)
                if newcsbans.getnextBan() == ctx.message.author.name:
                    msg = newcsbans.processBan()
                    sent = await client.send_message(ctx.message.author, msg)
                    i = 0
                    for x, y in newcsbans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            await client.add_reaction(sent, emoji)
                            i += 1
                    reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'], message=sent,
                    check=lambda reaction, user: user == ctx.message.author)
                    msg = newcsbans.banpick(reaction2.index(reaction.reaction.emoji))
                    await client.send_message(ctx.message.author, msg)
                    await client.send_message(member, msg)
                elif str(newcsbans.getnextBan()) == str(member.name):                    
                    msg = newcsbans.processBan()
                    sent = await client.send_message(member, msg)
                    i = 0
                    for x, y in newcsbans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            await client.add_reaction(sent, emoji)
                            i += 1
                    reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'], message=sent,
                    check=lambda reaction, user: user == member)
                    msg = newcsbans.banpick(reaction2.index(reaction.reaction.emoji))
                    await client.send_message(ctx.message.author, msg)
                    await client.send_message(member, msg)                        
            await client.send_message(ctx.message.author, newcsbans.getRemainingMaps())
            await client.send_message(member, newcsbans.getRemainingMaps())
            for server in client.servers:
                for channel in server.channels:
                    if int(channel.id) == 721312912630611968:
                        textchannel = channel
            await client.send_message(textchannel, newcsbans.getHistory())
            await client.send_message(textchannel, newcsbans.getRemainingMaps())

        if newcsbans.getBestof() == 3:
            reaction2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
            while newcsbans.checkMaps() >= 2:
              
                print(newcsbans.getnextBan(), member.name)
                if newcsbans.getnextBan() == ctx.message.author.name:
                    msg = newcsbans.processBan()
                    sent = await client.send_message(ctx.message.author, msg)
                    i = 0
                    for x, y in newcsbans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            await client.add_reaction(sent, emoji)
                            i += 1
                    reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'], message=sent,
                    check=lambda reaction, user: user == ctx.message.author)
                    msg = newcsbans.banpick(reaction2.index(reaction.reaction.emoji))
                    await client.send_message(ctx.message.author, msg)
                    await client.send_message(member, msg)     
                elif str(newcsbans.getnextBan()) == str(member.name):
                    msg = newcsbans.processBan()
                    sent = await client.send_message(member, msg)
                    i = 0
                    for x, y in newcsbans.getAllmaps().items():
                        if y is "neutral":
                            emoji = reaction2[i]
                            await client.add_reaction(sent, emoji)
                            i += 1
                    reaction = await client.wait_for_reaction(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'], message=sent,
                    check=lambda reaction, user: user == member)
                    msg = newcsbans.banpick(reaction2.index(reaction.reaction.emoji))
                    await client.send_message(ctx.message.author, msg)
                    await client.send_message(member, msg)     
            await client.send_message(ctx.message.author, newcsbans.getRemainingMaps())
            await client.send_message(member, newcsbans.getRemainingMaps())    
            for server in client.servers:
                for channel in server.channels:
                    if int(channel.id) == 721312912630611968:
                        textchannel = channel
            await client.send_message(textchannel, newcsbans.getHistory())
            await client.send_message(textchannel, newcsbans.getRemainingMaps())         

    else:
        print("member not found")
        await client.send_message(ctx.message.author, "The discord user you inputted cannot be found.")

@client.command(pass_context=True)
async def close(ctx):
    if ctx.message.author.server_permissions.administrator:
        exit()
    else:
        await client.say("You need to be an administrator!")
client.run(TOKEN)  