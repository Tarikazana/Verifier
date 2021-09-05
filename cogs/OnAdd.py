"""
> OnAdd.py
> Author: Tari Kazana
> First instructions

"""

import discord
import json
from discord.ext import commands
from datetime import datetime


class OnAdd(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
        with open('verifier/config.json', 'r') as config:
            conf = json.load(config)
            pref = conf["prefix"]

        embed=discord.Embed(title="Thank you for adding this bot to your server", description="", color=0xffa501)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Setup", value="start the setup by typing "+pref+"setup", inline=False)
        
        embed.set_footer(text="Verifier | Developed by Tari#7072")

        if guild.system_channel:
            await guild.system_channel.send(embed=embed)
        else:
            pass


def setup(bot:commands.Bot):
    bot.add_cog(OnAdd(bot))