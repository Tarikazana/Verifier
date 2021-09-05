"""
> help.py
> Author: Tari Kazana
> does the helping thing

"""

import discord
import json
from discord.ext import commands
from datetime import datetime


class help(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "help")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def commandName(self, ctx:commands.Context):
        with open('verifier/config.json', 'r') as config:
            conf = json.load(config)
            pref = conf["prefix"]
        embed=discord.Embed(title="Help", description=f"Commands:", color=0xffa501)
        embed.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))

        embed.add_field(name=f"{pref}setup", value="set the bot up to have it work properly", inline=False)
        embed.add_field(name=f"{pref}questions", value="set the questions the bot asks", inline=False)
        embed.add_field(name=f"{pref}verify", value="starts the verification with the set questions in dms of the user", inline=False)
        embed.add_field(name=f"{pref}welcomemsg", value="set/activate welcome message", inline=False)
        embed.add_field(name=f"{pref}approve", value="approve users and send them a welcomemessage", inline=False)
        embed.add_field(name=f"{pref}invite", value="invite this bot to your server!", inline=False)

        embed.timestamp = datetime.now()
        embed.set_footer(text="Verifier | Developed by Tari#7072")
        await ctx.send(embed=embed)


def setup(bot:commands.Bot):
    bot.add_cog(help(bot))
