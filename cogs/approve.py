"""
> approve.py
> Author: Tari Kazana
> approve users

"""

import json
import discord
from discord.ext import commands
from datetime import datetime


class approve(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "approve")
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def commandName(self, ctx:commands.Context, user:discord.Member):
        with open(f"verifier/data/server/wm_{ctx.guild.id}.json", 'r') as wm_file:
            wmfile = json.load(wm_file)
            ver_role_id = wmfile["ver_role_id"]
            general_chat_id = wmfile["general_chat_id"]
            welcomemsg = wmfile["wm"]

        guild=ctx.guild
        for x in guild.roles:
            if str(x.id) == str(ver_role_id):
                ver_role = x
                pass

        general_chat=self.bot.get_channel(int(general_chat_id))

        if ver_role in user.roles:
            await ctx.message.delete()
            await ctx.send(f"{user.name} is already verified")
            return
        else:
            await user.add_roles(ver_role)
            
        await ctx.message.delete()
        await ctx.send(f"`// {ctx.author} approved {user.id} //`")
        await user.send(f"Heya! {ctx.author.display_name} just approved you :3")

        welcomemsg = str(welcomemsg).replace("$user",f"{user}")

        embed=discord.Embed(title=f"__Welcome {user.name}!__", description=str(welcomemsg), color=0xffa501)
        embed.timestamp = datetime.now()
        embed.set_footer(text="Verifier | Developed by Tari#7072")
        embed.set_thumbnail(url=user.avatar_url)
        await general_chat.send(embed=embed)





def setup(bot:commands.Bot):
    bot.add_cog(approve(bot))