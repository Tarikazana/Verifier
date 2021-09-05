"""
> questions.py
> Author: Tari Kazana
> saving questions to database

"""

import discord
import json
import asyncio
import os
from datetime import datetime
from discord.ext import commands


class questions(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "questions")
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def commandName(self, ctx:commands.Context):
        with open('verifier/config.json', 'r') as config:
            conf = json.load(config)
            pref = conf["prefix"]

        def check(message, ctx=ctx):
            return message.author == ctx.author and message.channel == ctx.channel
        done = False
        i=1
        questions = []
        while done == False:
            await ctx.send(f"{ctx.author.mention} Please send me question {i}\n*if done send 'done'; to cancel send 'cancel'*")
            try:    
                msg = await self.bot.wait_for('message', check=check, timeout = 300)
                if str(msg.content).lower() == "done":
                    done = True
                elif str(msg.content).lower() == "cancel":
                    await ctx.send("canceled.")
                    return
                else:
                    questions.append(str(msg.content).replace('"',"'"))
            except asyncio.TimeoutError:
                await ctx.send("`You took too long to answer. Discarding questions.`")
                done == True
                return
            i+=1

        await ctx.send(f"Your questions are:")
        loq = ""
        for x in questions:
            loq = loq + "-> "+str(x)+"\n"

        await ctx.send("```\n"+loq+"```")

        await ctx.send("Are those correct? Y/N")
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
            await ctx.send("`You took too long to answer. Discarding questions.`")
            return

        if not os.path.isfile(f"verifier/data/server/questions_{ctx.guild.id}.json"):
            open(f"verifier/data/server/questions_{ctx.guild.id}.json", "a").close()
            await ctx.send(f"```asciidoc\n[debug]\n>> Created new file```")

        loq = ""
        i=1
        for x in questions:
            loq = loq + f'"{str(i)}":"{str(x)}",'
            i+=1
        loq = loq[:-1].replace("'","")

        idDict = "{"+f"{loq}"+"}"

        jsonString = json.dumps(idDict)
        jsonString = jsonString.replace("\\","")[1:-1]
        jsonFile = open(f"verifier/data/server/questions_{ctx.guild.id}.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        await ctx.send(f"```asciidoc\n[debug]\n>> Questions saved```")
        with open(f"verifier/data/server/{ctx.guild.id}.json", 'r') as f:
            idfile = json.load(f)
            ver_id = idfile["verification_channel_id"]
            mod_id = idfile["mod_channel_id"]
        ver_channel=self.bot.get_channel(ver_id)
        mod_channel=self.bot.get_channel(mod_id)   
        await ctx.send(f"Nice! Users can now verify by using {pref}verify in {ver_channel.mention}\nApplications will be send to {mod_channel.mention}\nSetup a welcomemessage with {pref}welcomemsg!")

def setup(bot:commands.Bot):
    bot.add_cog(questions(bot))