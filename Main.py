import base64

from discord.ext import commands
import discord
import requests
import io
import aiohttp

# FIRST API
headers = {
    'Accept': 'application/json'
}

# DISCORD BOT
bot = commands.Bot(command_prefix='-')

# DEFAULT EVENT CODE
event_code = 'TXPLA'
event_name = 'FIT District Plano Event'


@bot.command()
async def helpme(ctx):
    embed = discord.Embed(color=discord.Color.from_rgb(128, 0, 0),
                          title='Here are the available commands:')
    embed.add_field(name='-set_event', value='Example: -set_event TXPLA',
                    inline=False)
    embed.add_field(name='-event_info', value='Example: -event_info',
                    inline=False)
    embed.add_field(name='-team_info', value='Example: -team_info 6171 :sunglasses:',
                    inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def set_event(ctx, arg):
    try:
        global event_code
        event_code = arg.upper()

        name = requests.get('https://frc-api.firstinspires.org/v2.0/2020/events?eventCode=' + event_code,
                            headers=headers, auth=('stikcye', '9933C5D2-F724-428F-B4A6-6A8978A3F251')).json()
        global event_name
        event_name = name['Events'][0]['name']

        embed = discord.Embed(color=discord.Color.from_rgb(128, 0, 0),
                              title='You have set the event!')
        embed.add_field(name='Event name:',
                        value=event_name, inline=True)
        embed.add_field(name='Event code:',
                        value=event_code, inline=True)
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(color=discord.Color.from_rgb(128, 0, 0),
                              title='You are missing a parameter!')
        embed.add_field(name='Example:',
                        value='-set_event txpla', inline=True)
        await ctx.send(embed=embed)


@bot.command()
async def event_info(ctx):
    rankings = requests.get('https://frc-api.firstinspires.org/v2.0/2020/rankings/' + event_code + '?',
                            headers=headers, auth=('', '')).json()
    teams = requests.get('https://frc-api.firstinspires.org/v2.0/2020/teams?eventCode=' + event_code,
                         headers=headers, auth=('', '')).json()
    amount_of_teams = teams['teamCountTotal']
    print(amount_of_teams)
    print_array = []

    # discord embed
    embed = discord.Embed(color=discord.Color.from_rgb(128, 0, 0),
                          title='Here are the rankings at ' + event_name)
    embed_extra = discord.Embed(color=discord.Color.from_rgb(128, 0, 0), title=' ')

    # add to array of team_number and team_rank
    for i in range(0, amount_of_teams):
        team_number = str(rankings['Rankings'][i]['teamNumber'])
        team_rank = rankings['Rankings'][i]['rank']

        # endings here
        if (team_rank % 10) == 0 or (team_rank % 10) >= 4 or (11 <= team_rank <= 13):
            ending = 'th'
        elif (team_rank % 10) == 1:
            ending = 'st'
        elif (team_rank % 10) == 2:
            ending = 'nd'
        elif (team_rank % 10) == 3:
            ending = 'rd'

        if i < 25:
            embed.add_field(name=str(team_rank) + str(ending),
                            value=team_number, inline=True)
        else:
            embed_extra.add_field(name=str(team_rank) + str(ending),
                                  value=team_number, inline=True)

        # print_array.append(team_number + ' is in ' + str(team_rank) + ending + ' place.')

    # send message
    # await ctx.send(
    # 'there are ' + str(amount_of_teams) + ' at the ' + str(event_code) + ' event. here are their rankings.')
    # await ctx.send('\n'.join(print_array))
    await ctx.send(embed=embed)
    if amount_of_teams > 25:
        await ctx.send(embed=embed_extra)


@bot.command()
async def team_info(ctx, arg):
    rank = requests.get('https://frc-api.firstinspires.org/v2.0/2020/rankings/' + event_code + '?teamNumber=' + arg,
                        headers=headers, auth=('', '')).json()
    avatar_encoded = requests.get('https://frc-api.firstinspires.org/v2.0/2020/avatars?teamNumber=' + arg,
                                  headers=headers, auth=('', '')).json()
    team_name = requests.get('https://frc-api.firstinspires.org/v2.0/2020/teams?teamNumber=' + arg,
                            headers=headers, auth=('', '')).json()['teams'][0]['nameShort']

    int_ranking = rank['Rankings'][0]['rank']
    ranking = str(rank['Rankings'][0]['rank'])

    wins = str(rank['Rankings'][0]['wins'])
    losses = str(rank['Rankings'][0]['losses'])
    ties = str(rank['Rankings'][0]['ties'])

    avatar = avatar_encoded['teams'][0]['encodedAvatar']

    qual_average = str(rank['Rankings'][0]['qualAverage'])

    # endings here
    ending = None
    if (int_ranking % 10) == 0 or (int_ranking % 10) >= 4 or (11 <= int_ranking <= 13):
        ending = 'th'
    elif (int_ranking % 10) == 1:
        ending = 'st'
    elif (int_ranking % 10) == 2:
        ending = 'nd'
    elif (int_ranking % 10) == 3:
        ending = 'rd'

    # embed lines
    embed = discord.Embed(color=discord.Color.from_rgb(128, 0, 0), title='Here is the team info you requested!')

     embed.add_field(name=f'The ranking for team ' + arg + ' ' +  team_name + ' at the ' + event_name + ' event.', value=ranking + ending,
                    inline=False)
    embed.add_field(name=f'They have won:', value=wins + ' match(es).',
                    inline=False)
    embed.add_field(name=f'They have lost:', value=losses + ' match(es).',
                    inline=False)
    embed.add_field(name=f'They have tied:', value=ties + ' match(es).',
                    inline=False)
    embed.add_field(name=f'The team\'s qual average:', value=qual_average + ' points.',
                    inline=False)

    avatar = bytes(avatar, 'utf8')
    avatar_poop = base64.decodebytes(avatar)

    file = discord.File(io.BytesIO(avatar_poop), filename="avayar.png")
    embed.set_thumbnail(url="attachment://avayar.png")

    # send message
    await ctx.send(file=file, embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=discord.Color.from_rgb(128, 0, 0), title=' ')
        embed.add_field(name=f'You are missing an argument!', value='EX: -team_info -->6171<--',
                        inline=False)
        await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print('Bot is Online: ID:', bot.user.id)


bot.run('')
