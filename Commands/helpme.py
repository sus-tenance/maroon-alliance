import discord
from discord.ext import commands


# authors: stickyee and joshuathooyavan

class HELPME(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helpme(self, ctx):
        embed = discord.Embed(color=discord.Color.from_rgb(128, 0, 0),
                              title='Here are the available commands:')
        embed.add_field(name='-set_event', value='Example: -set_event TXPLA',
                        inline=False)
        embed.add_field(name='-event_info', value='Example: -event_info',
                        inline=False)
        embed.add_field(name='-team_info', value='Example: -team_info 6171 :sunglasses:',
                        inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HELPME(bot))
