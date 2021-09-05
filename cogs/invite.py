"""
> invite.py
> Author: Tari Kazana
> send inv link to user

"""

import discord
from discord.ext import commands


class invite(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "invite")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 86400, commands.BucketType.member)
    async def commandName(self, ctx:commands.Context):
        info = await self.bot.application_info()
        Tari = info.owner

        await ctx.author.send("Hey! Here is the invite link you requested!\nhttps://your-link-here")

        await ctx.reply("Hey! I sent the invite link you requested in your DMs!")
        
        await Tari.send(f"```asciidoc\n[info]\nInvite link was requested by {ctx.author} ({ctx.author.id})```")


def setup(bot:commands.Bot):
    bot.add_cog(invite(bot))