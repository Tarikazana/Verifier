"""
> error.py
> Author: Tari Kazana
> cooldown and stuff

"""

import discord
import traceback
import sys
import math
import asyncio
from discord.ext import commands


class err(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # if command has local error handler, return
        if hasattr(ctx.command, 'on_error'):
            return

        # get the original exception
        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
            await ctx.reply(_message)
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.reply('This command has been disabled.')
            return

        if isinstance(error, commands.CommandOnCooldown):
            time = math.ceil(error.retry_after)
            
            if time > 3600:
                h = 0
                while time > 3600:
                    time = time - 3600
                    h = h + 1

                i = 0
                while time > 60:
                    time = time - 60
                    i = i + 1
                
                time = "{h} {hours}, {i} {minutes} and {time} {seconds}".format(h=h, i=i, time=time, hours="hour" if h == 1 else "hours", minutes="minute" if i == 1 else "minutes", seconds="second" if time == 1 else "seconds") 
            elif time > 60:
                i = 0
                while time > 60:
                    time = time - 60
                    i = i + 1

                time = "{i} {minutes} and {time} {seconds}".format(i=i, time=time, minutes="minute" if i == 1 else "minutes", seconds="second" if time == 1 else "seconds")
            else:
                pass

            await ctx.reply("Please wait {} before using this again".format(time))
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            await ctx.reply(_message)
            return

        if isinstance(error, commands.UserInputError):
            await ctx.reply("Invalid input.")
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send('This command cannot be used in direct messages.')
            except discord.Forbidden:
                pass
            return


        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        await ctx.reply(f'```Ignoring exception in command {ctx.command}:\nerror: {error}```')


def setup(bot):
    bot.add_cog(err(bot))