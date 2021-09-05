"""
> setup.py
> Author: Tari Kazana
> saving channels to database

"""

import discord
import json
import asyncio
import os
from datetime import datetime
from discord.ext import commands


class setupbot(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "setup")
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def commandName(self, ctx:commands.Context):
        with open('verifier/config.json', 'r') as config:
            conf = json.load(config)
            pref = conf["prefix"]

        await ctx.send(f"{ctx.author.mention} Please send me the verification channel")
        def check(message, ctx=ctx):
            return message.author == ctx.author and message.channel == ctx.channel
        try:    
            msg1 = await self.bot.wait_for('message', check=check, timeout = 300)
            verification_channel_id=int(str(msg1.content).replace("<#","").replace(">",""))
        except asyncio.TimeoutError:
            await ctx.author.send("You took too long to answer.")
            return
        except ValueError:
            await ctx.send(f"{ctx.author.mention} Please make sure to send me a valid format (e.g. #general)")
            try:    
                msg1 = await self.bot.wait_for('message', check=check, timeout = 300)
                verification_channel_id=int(str(msg1.content).replace("<#","").replace(">",""))
            except asyncio.TimeoutError:
                await ctx.author.send("You took too long to answer.")
                return

        if not os.path.isfile(f"verifier/data/server/{ctx.guild.id}.json"):
            open(f"verifier/data/server/{ctx.guild.id}.json", "a").close()
            await ctx.send(f"```asciidoc\n[debug]\n>> Created new file```")

        channel=self.bot.get_channel(verification_channel_id)
        await ctx.send(f"Added Channel {channel.mention} as verification channel.")
        await ctx.send(f"{ctx.author.mention} Please send me the moderation channel")
        try:    
            msg2 = await self.bot.wait_for('message', check=check, timeout = 300)
            mod_channel_id=int(str(msg2.content).replace("<#","").replace(">",""))
        except asyncio.TimeoutError:
            await ctx.author.send("You took too long to answer.")
            return
        except ValueError:
            await ctx.send(f"{ctx.author.mention} Please make sure to send me a valid format (e.g. #general)")
            try:    
                msg2 = await self.bot.wait_for('message', check=check, timeout = 300)
                mod_channel_id=int(str(msg2.content).replace("<#","").replace(">",""))
            except asyncio.TimeoutError:
                await ctx.author.send("You took too long to answer.")
                return  

        channel=self.bot.get_channel(mod_channel_id)
        await ctx.send(f"Added Channel {channel.mention} as moderation channel.")
        idDict = {"verification_channel_id":verification_channel_id, "mod_channel_id":mod_channel_id}
        jsonString = json.dumps(idDict)
        jsonFile = open(f"verifier/data/server/{ctx.guild.id}.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()


        with open(f"verifier/data/server/{ctx.guild.id}.json", 'r') as f:
            idfile = json.load(f)
            ver_id = idfile["verification_channel_id"]
            mod_id = idfile["mod_channel_id"]

        await ctx.send(f"```asciidoc\n[debug]\n>> written to file: ver_id:{ver_id}/mod_id:{mod_id}```")

        await ctx.send(f"{ctx.author.mention} Please go ahead and set your questions with {pref}questions")


def setup(bot:commands.Bot):
    bot.add_cog(setupbot(bot))