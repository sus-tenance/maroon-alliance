import base64
import io

import discord
import requests
from discord.ext import commands

import config

# authors: stickyee and joshuathooyavan

# FIRST API
headers = {
    'Accept': 'application/json'
}

# DEFAULT EVENT CODE
# event_name = 'FIT District Plano Event'
# event_code = 'TXPLA'

event_code_dic = {}
event_name_dic = {}


class EVENTCOMMANDS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_event(self, ctx, arg):
        temp_id = ctx.guild.id

        global event_code_dic
        event_code_dic[temp_id] = str(arg.upper())
        event_code = str(event_code_dic[temp_id])
        print(str(event_code_dic[temp_id]))

        event_name = requests.get('https://frc-api.firstinspires.org/v2.0/2020/events?eventCode=' + event_code,
                                  headers=headers, auth=(config.username, config.password)).json()['Events'][0]['name']

        global event_name_dic
        event_name_dic[temp_id] = event_name

        embed = discord.Embed(color=discord.Color.from_rgb(128, 0, 0),
                              title='You have set the event!')
        embed.add_field(name='Event name:',
                        value=event_name, inline=True)
        embed.add_field(name='Event code:',
                        value=event_code, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def event_info(self, ctx):
        temp_id = ctx.guild.id

        global event_code_dic
        event_code = str(event_code_dic[temp_id])

        # gets the data we need from the FIRST API in json form.
        rankings = requests.get('https://frc-api.firstinspires.org/v2.0/2020/rankings/' + event_code + '?',
                                headers=headers, auth=(config.username, config.password)).json()
        teams = requests.get('https://frc-api.firstinspires.org/v2.0/2020/teams?eventCode=' + event_code,
                             headers=headers, auth=(config.username, config.password)).json()
        amount_of_teams = teams['teamCountTotal']
        print(amount_of_teams)

        global event_name_dic
        event_name = event_name_dic[temp_id]

        # discord create embeds.
        embed = discord.Embed(color=discord.Color.from_rgb(128, 0, 0),
                              title='Here are the rankings at ' + event_name)
        embed_extra = discord.Embed(color=discord.Color.from_rgb(128, 0, 0), title=' ')

        # loops through the API response to find all the teams and their numbers in the set event.
        for i in range(0, amount_of_teams):
            team_number = rankings['Rankings'][i]['teamNumber']
            team_rank = rankings['Rankings'][i]['rank']

            # statement to find out what embed field to add the data to depending on the amount of teams.
            if i < 25:
                embed.add_field(name=str(team_rank) + endings(team_rank),
                                value=str(team_number), inline=True)
            else:
                embed_extra.add_field(name=str(team_rank) + endings(team_rank),
                                      value=str(team_number), inline=True)

        # if this is inside of the loop cursed things happen, trust me, I know.
        await ctx.send(embed=embed)
        if amount_of_teams > 25:
            await ctx.send(embed=embed_extra)

    @commands.command()
    async def team_info(self, ctx, arg):
        temp_id = ctx.guild.id

        global event_code_dic
        event_code = str(event_code_dic[temp_id])

        # gets the data we need from the FIRST API in json form.
        rank = requests.get('https://frc-api.firstinspires.org/v2.0/2020/rankings/' + event_code + '?teamNumber=' + arg,
                            headers=headers,
                            auth=(config.username, config.password)).json()
        team_name = requests.get('https://frc-api.firstinspires.org/v2.0/2020/teams?teamNumber=' + arg, headers=headers,
                                 auth=(config.username, config.password)).json()['teams'][0]['nameShort']
        avatar_encoded = requests.get('https://frc-api.firstinspires.org/v2.0/2020/avatars?teamNumber=' + arg,
                                      headers=headers,
                                      auth=(config.username, config.password)).json()

        ranking = rank['Rankings'][0]['rank']
        wins = str(rank['Rankings'][0]['wins'])
        losses = str(rank['Rankings'][0]['losses'])
        ties = str(rank['Rankings'][0]['ties'])
        avatar = avatar_encoded['teams'][0]['encodedAvatar']
        qual_average = str(rank['Rankings'][0]['qualAverage'])

        global event_name_dic
        event_name = event_name_dic[temp_id]

        # create discord embeds.
        embed = discord.Embed(color=discord.Color.from_rgb(128, 0, 0), title='Here is the team info you requested!')

        embed.add_field(name=f'The ranking for team ' + arg + ' ' + team_name + ' at the ' + event_name + ' event.',
                        value=str(ranking) + endings(ranking),
                        inline=False)
        embed.add_field(name=f'They have won:', value=wins + ' match(es).',
                        inline=False)
        embed.add_field(name=f'They have lost:', value=losses + ' match(es).',
                        inline=False)
        embed.add_field(name=f'They have tied:', value=ties + ' match(es).',
                        inline=False)
        embed.add_field(name=f'The team\'s qual average:', value=qual_average + ' points.',
                        inline=False)

        # sets the avatar of the team specified and converts it so discord can read and use it.
        avatar = bytes(avatar, 'utf8')
        avatar_poop = base64.decodebytes(avatar)
        file = discord.File(io.BytesIO(avatar_poop), filename="avatar.png")
        embed.set_thumbnail(url="attachment://avatar.png")

        await ctx.send(file=file, embed=embed)


def endings(number):
    ending = None
    if (number % 10) == 0 or (number % 10) >= 4 or (11 <= number <= 13):
        ending = 'th'
    elif (number % 10) == 1:
        ending = 'st'
    elif (number % 10) == 2:
        ending = 'nd'
    elif (number % 10) == 3:
        ending = 'rd'
    return ending


def setup(bot):
    bot.add_cog(EVENTCOMMANDS(bot))
