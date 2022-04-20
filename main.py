import discord
import os
import requests
from discord.ext import commands
import datetime

bot = commands.Bot(command_prefix='!')

url = "https://api-football-v1.p.rapidapi.com/v3"

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "37a787ee2emsh8ff5831108b0f21p1f86c7jsn65cde3ad31cd"
}


def getAPI(path, query):
    try:
        response = requests.get(url=f"{url}/{path}",
                                headers=headers,
                                params=query)
        json_data = response.json()
        print(json_data)
        if not 'response' in json_data.keys():
          raise Exception('invalid response!')
        response = json_data['response']
        return response
    except:
        return None


def getStandingsById(id,year):
    data = {}
    if not year:
      date = datetime.date.today()
      year = date.strftime("%Y") 
    querystring = {"season": year, "league": id}
    response = getAPI('standings', querystring)
    if not response: return None
    for item in response:
        league = item['league']
        data['league_name'] = league['name']
        standings = league['standings']
        for standing in standings:
            data['standings'] = standing
            return data




@bot.command(name='standings')
async def standings(ctx, league_id, year=None):
    data = getStandingsById(league_id, year)
    if not data:
        await ctx.channel.send('No data!')
    else:
        standings = data['standings']
        league_name = data['league_name']
        embed = discord.Embed(title=f'**{league_name} Standings**',
                              color=0xe51010)
        for line in standings:
            embed.add_field(name='Rank {rank}'.format(rank=line['rank']),
                            value=line['team']['name'],
                            inline=False)
        await ctx.channel.send(embed=embed)


def searchleagueByKey(keywords):
    queries = {"search": keywords}
    response = getAPI('leagues', queries)
    return response

def searchteamByKey(keywords):
    queries = {"search": keywords}
    response = getAPI('teams', queries)
    return response



@bot.command(name='search')
async def search(ctx,*keywords):
    keywords = ' '.join(keywords)
    data = searchleagueByKey(keywords)
    data1 = searchteamByKey(keywords)
    if not data and not data1:
        await ctx.channel.send('No data!')
    else:
        embed = discord.Embed(title=f'**Search results for** *{keywords}*',
                              color=0xe51010)
        if data:
          for item in data:
            league = item['league']
            country = item['country']
            embed.add_field(name='{name}'.format(name=league['name'],), value='ID: {id} \n Country: {country}' .format(
                    id=league['id'],
                    country=country['name'],
                    inline=False))
        if data1:
          for item in data1:
            team = item['team']
            embed.add_field(name='{name}'.format(name=team['name'],), value= 'ID: {id} \n Country: {country}'.format(
                   id=team['id'],
                   country=team['country'],
                   inline=False))
        await ctx.channel.send(embed=embed)
    

bot.run(os.getenv('TOKEN'))


