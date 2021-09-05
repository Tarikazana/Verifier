"""
> OnRemove.py
> Author: Tari Kazana
> Updating configs

"""

import discord
import json
import os
from discord.ext import commands


class OnLeave(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild:discord.Guild):
        if os.path.isfile(f'verifier/data/server/{guild.id}.json'):
            os.remove(f"verifier/data/server/{guild.id}.json")
        if os.path.isfile(f'verifier/data/server/questions_{guild.id}.json'):
            os.remove(f"verifier/data/server/questions_{guild.id}.json")

def setup(bot:commands.Bot):
    bot.add_cog(OnLeave(bot))