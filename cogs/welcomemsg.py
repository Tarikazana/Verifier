"""
> welcomemsg.py
> Author: Tari Kazana
> welcome message

"""

import asyncio
import json
import os
import discord
from discord.ext import commands


class welcomemsg(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "welcomemsg")
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def commandName(self, ctx:commands.Context):
        def check(message, ctx=ctx):
            return message.author == ctx.author and message.channel == ctx.channel
        if os.path.isfile(f"verifier/data/server/wm_{ctx.guild.id}.json"):
            await ctx.send("Overwrite welcome message? Y/N")
        else:
            await ctx.send("This message will be send after users have been approved. It requires you to have setup a role the bot can assign to users after verification.\nActivate welcome message? Y/N")
        try:    
            msg = await self.bot.wait_for('message', check=check, timeout = 300)
            if str(msg.content).lower() == "y" or str(msg.content).lower() == "yes":
                pass
            elif str(msg.content).lower() == "n" or str(msg.content).lower() == "no":
                await ctx.send("canceled.")
                return
            else:
                await ctx.send("Could not process answer | canceled.")
                return
        except asyncio.TimeoutError:
            await ctx.send("`You took too long to answer. Canceled.`")
            return

        await ctx.send("Please @ the role users shall get assigned when approved:")
        try:    
            msg1 = await self.bot.wait_for('message', check=check, timeout = 300)
        except asyncio.TimeoutError:
            await ctx.send("`You took too long to answer. Canceled.`")
            return
        ver_role_id = str(msg1.content).replace("<@&","").replace(">","")

        await ctx.send("You might aswell tag me the general chat so I know where to send the welcome message (e.g. #general):")
        try:    
            msg2 = await self.bot.wait_for('message', check=check, timeout = 300)
        except asyncio.TimeoutError:
            await ctx.send("`You took too long to answer. Canceled.`")
            return
        general_chat_id = str(msg2.content).replace("<#","").replace(">","")

        await ctx.send("Please write your welcome message. Use $user as placeholder for the username. E.g. 'welcome $user!'")
        try:    
            msg3 = await self.bot.wait_for('message', check=check, timeout = 300)
        except asyncio.TimeoutError:
            await ctx.send("`You took too long to answer. Canceled.`")
            return
        if not os.path.isfile(f"verifier/data/server/wm_{ctx.guild.id}.json"):
            open(f"verifier/data/server/wm_{ctx.guild.id}.json", "a").close()
            await ctx.send(f"```asciidoc\n[debug]\n>> Created new file```")
            
        idDict = '{"wm":'+f'"{str(msg3.content)}'+'", "ver_role_id":'+f'"{str(ver_role_id)}'+'", "general_chat_id":'+f'"{str(general_chat_id)}'+'"}'
        jsonString = json.dumps(idDict)
        jsonString = jsonString.replace("\\","")[1:-1]
        jsonFile = open(f"verifier/data/server/wm_{ctx.guild.id}.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        await ctx.send(f"```asciidoc\n[debug]\n>> Welcome message saved```")



def setup(bot:commands.Bot):
    bot.add_cog(welcomemsg(bot))