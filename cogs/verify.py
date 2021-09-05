"""
> verify.py
> Author: Tari Kazana
> user DMs

"""

import discord
import json
import asyncio
import os
from discord.ext import commands
from datetime import datetime


class verify(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "verify")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 900, commands.BucketType.member)
    async def commandName(self, ctx:commands.Context):
        if not os.path.isfile(f"verifier/data/server/questions_{ctx.guild.id}.json"):
            await ctx.send(f"{ctx.author.mention} Setup not complete. Run --setup!", delete_after=2)
            return
        with open(f"verifier/data/server/questions_{ctx.guild.id}.json", 'r') as question_file:
            qfile = json.load(question_file)
            len_qfile = len(qfile)
            i=1
            questions = []
            for i in range(1, len_qfile+1):
                questions.append(qfile[str(i)])      
        
        with open(f"verifier/data/server/{ctx.guild.id}.json", 'r') as id_file:
            idfile = json.load(id_file)
            ver_id = idfile["verification_channel_id"]
            mod_id = idfile["mod_channel_id"]
        ver_channel=self.bot.get_channel(ver_id)
        mod_channel=self.bot.get_channel(mod_id)

        if not ctx.channel == ver_channel:
            await ctx.send(f"{ctx.author.mention} You can't use that here!", delete_after=2)
            return
        
        await ctx.send(f"`@{ctx.author} > Testing DMs...`", delete_after=5)
        try:
            await ctx.author.send("_ _", delete_after=0)
        except:
            await ctx.send(f"{ctx.author.mention} Please enable DMs.")
            return

        embed=discord.Embed(title="", description=f"Verification from {ctx.author.name} started.", color=0xffa501)
        embed.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
        embed.timestamp = datetime.now()
        embed.set_footer(text="Verifier | Developed by Tari#7072")
        async with ctx.typing():
            await ctx.send(embed=embed)
            await ctx.send(f"{ctx.author.mention} Check your DMs!", delete_after=2)

        await ctx.author.send(f"Hey there! Welcome to {ctx.guild.name}. We'd like to ask you a few questions before you enter our Server.")
        await asyncio.sleep(1)
        def check(message, ctx=ctx):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

        a = []
        for x in questions:
            await ctx.author.send(str(x))
            try:    
                msg = await self.bot.wait_for('message', check=check, timeout = 300)
                a.append(str(msg.content))
            except asyncio.TimeoutError:
                await ctx.author.send("`You took too long to answer. Please restart the verification.`")
                embed=discord.Embed(title="Timeout", description=f"Verification from {ctx.author.name} canceled.", color=0x94196d)
                embed.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
                embed.timestamp = datetime.now()
                embed.set_footer(text="Verifier | Developed by Tari#7072")
                await ctx.send(embed=embed)
                return
        await ctx.author.send("Thank you. Please give us some time to review your answers.")
        
        embed=discord.Embed(title=f"__Verification from {ctx.author.name}__", description="Please review the following", color=0xffa501)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
        i=0
        for x in questions:
            embed.add_field(name=str(x), value="Answer: "+a[i], inline=False)
            i+=1
        embed.timestamp = datetime.now()
        embed.set_footer(text="Verifier | Developed by Tari#7072")

        await mod_channel.send(embed=embed)
        




def setup(bot:commands.Bot):
    bot.add_cog(verify(bot))