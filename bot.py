from discord.ext import commands
import discord
import config

# authors: stickyee and joshuathooyavan

# DISCORD BOT
startup_extensions = ["Commands.event_commands", "Commands.helpme"]
bot = commands.Bot(command_prefix=config.bot_prefix)


# errors can be specified here.
@bot.event
async def on_command_error(ctx, error):
    # if there is a missing argument for any command the below statement is run.
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=discord.Color.from_rgb(128, 0, 0), title=' ')
        embed.add_field(name=f'You are missing an argument!', value='Please try again, but with something after the command :sunglasses:',
                        inline=False)
        await ctx.send(embed=embed)
    if isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(color=discord.Color.from_rgb(128, 0, 0), title=' ')
        embed.add_field(name=f'Oh no!', value='Something went wrong, please try again.\nPossible issue: Invalid argument or no event code set..',
                        inline=False)
        await ctx.send(embed=embed)
    # more errors can be added below.


@bot.event
async def on_ready():
    print('Bot is Online:', bot.user.name)
    for extension in startup_extensions:
        bot.load_extension(extension)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="-helpme"), status=discord.Status.dnd)


bot.run(config.bot_key)
