# -*- coding: utf-8 -*-
import requests
import random

file = open("E:\\Projects\\Python\\bot.txt", "r")
tokens = file.readlines()

client_id = tokens[3][:-1]
secret_key = tokens[5][:-1]
access_token = tokens[7][:-1]
header = {'Client-ID': f'{client_id}', 'Authorization': f'Bearer {access_token}'}
# REMAKE IGDb TOKEN
#header = {'client_id': f'{tokens[3][:-1]}', 'client_secret': f'{tokens[5][:-1]}', 'grant_type':'client_credentials'}
#print(requests.post('https://id.twitch.tv/oauth2/token', data = header).json())


def FindSimillarGame(gameName):
    value = f'search \"{gameName}\"; fields similar_games, name; where category = 0; limit 1;'
    responseGame = requests.post("https://api.igdb.com/v4/games", data = value, headers = header).json()
    originalGameId = responseGame[0]['id']
    print("NEW RESPONSE SIMILAR GAME")
    print(responseGame)
    print()
    if 'similar_games' in responseGame[0]: 
        similarGames = responseGame[0]['similar_games'] 
        value = f'fields similar_games, name; where id = ({str(similarGames)[1:-1]});'
        responseGame = requests.post("https://api.igdb.com/v4/games", data = value, headers = header).json()
        similarGames = []
        for similarArray in responseGame:
            for elem in similarArray['similar_games']:
                similarGames.append(elem)
        try:
            del similarGames[similarGames.index(originalGameId)]
        except Exception as exc:
            print(exc)
            pass
        print("NEW ARRAY SIMILAR GAME")
        print(similarGames)
        print()
        return similarGames
    else:
        return "No similar games found!"

def FindGamesById(game_id):
    try:
        value = f'fields: name, genres, cover, release_dates, rating, platforms, websites; where id = {game_id};'
        return UnpackJSON(requests.post("https://api.igdb.com/v4/games", data = value, headers = header).json())
    except Exception as exc:
        return "None"

def FindRandomGame(psycho):
    offset = 0
    if(psycho == False):
        offset = random.randint(0, 22000)
        value = f'fields: name, genres, cover, release_dates, rating, platforms, websites; limit: 1; offset: {offset}; where rating > 50;'
    else:
        offset = random.randint(0, 190000)
        value = f'fields: name, genres, cover, release_dates, rating, platforms, websites; limit: 1; offset: {offset};'
    return UnpackJSON(requests.post("https://api.igdb.com/v4/games", data = value, headers = header).json())

def UnpackJSON(responseGame):
    name = responseGame[0]["name"]
    cover = 'No info'
    genre = 'No info'
    websiteList = 'No info'
    releaseDate = 'No info\n'
    rating = 'No info'

    print('NEW UNPACK RESPONSE')
    print(responseGame)
    print()
    
    if 'cover' in responseGame[0]:
        cover = responseGame[0]['cover']
        responseCover = requests.post("https://api.igdb.com/v4/covers", data = f'fields url; where id = ({cover});', headers = header).json()
        cover = responseCover[0]['url']
        cover = str(cover).replace('t_thumb', 't_cover_big')

    if 'genres' in responseGame:
        genre = str(responseGame[0]['genres'])[1:-1]
        responseGenres = requests.post("https://api.igdb.com/v4/genres", data = f'fields name; where id = ({genre});', headers = header).json()
        genre = ''
        for i in responseGenres:
            genre += str(i['name']) + ', '
        genre = genre[:-2]
    
    if 'release_dates' in responseGame[0]:
        releaseDate = str((responseGame[0])['release_dates'])[1:-1]
        responseReleaseDates = requests.post('https://api.igdb.com/v4/release_dates', data = f'fields: human, platform; where id = ({releaseDate});', headers = header).json()
        releaseDate = ''
        for release in responseReleaseDates:
            releaseDate += str(release['platform']) + ', '
        releaseDate = releaseDate[:-2]
        responsePlatforms = requests.post('https://api.igdb.com/v4/platforms', data = f'fields name; where id = ({releaseDate});', headers = header).json()
        releaseDate = ''
        for release in responseReleaseDates:
            namePlatform = ''
            for namesPlatforms in responsePlatforms:
                if(release['platform'] == namesPlatforms['id']):
                    namePlatform = namesPlatforms['name']
                    break
            releaseDate += '\n' + release['human'] + ' (' + namePlatform + ')'
        releaseDate += "\n"

    if 'rating' in responseGame[0]:
        rating = str(int(responseGame[0]['rating'])) + ' / 100' 

    if 'websites' in responseGame[0]:
        websiteList = str(responseGame[0]['websites'])[1:-1]
        responseWebsites = requests.post('https://api.igdb.com/v4/websites', data = f'fields url; where id = ({websiteList});', headers = header).json()
        websiteList = responseWebsites[0]['url']

    return [f'{cover}', f'{name}', f'{genre}', f'{releaseDate}', f'{rating}', f'{websiteList}']
