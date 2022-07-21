# -*- coding: utf-8 -*-
import telebot
from telebot import types
import engine
import random

# Open file with tokens
file = open("E:\\Projects\\Python\\bot.txt", "r")
BOTtoken = file.readlines()
BOTtoken = BOTtoken[1][:-1]

bot = telebot.TeleBot(token = BOTtoken)

clientStatus = {}
similarGamesList = []


@bot.message_handler(commands=['start'])
def StartShowButton(message):
    clientId = message.chat.id
    bot.send_message(clientId, "Hello! I\'m SimillarBot.\nWrite /help to find out my functions", parse_mode = "Markdown")

@bot.message_handler(commands = ['help'])
def ShowHelp(message):
    clientId = message.chat.id
    bot.send_message(clientId,'Bot Commands\n' +
    '/rg - Find a random game with a higher rating 50\n' +
    '/vrg - Find a random game without a rating filter\n'
    '/like [name_game] - Find similar games by the title of the game')

@bot.message_handler(commands=['rg'])
def RandomGame(message):
    clientId = message.chat.id
    bot.send_message(clientId, text = "Your order in process! Wait a few second..", parse_mode = "Markdown")

    markupInline = types.InlineKeyboardMarkup()
    moreButton = types.InlineKeyboardButton("More..", callback_data="more_random_games")
    markupInline.add(moreButton)

    game = engine.FindRandomGame(False)
    sendText = f'🎮 Try play: *{game[1]}*\n\n🕹 Genres: *{game[2]}*\n\n📅 Release date: *{game[3]}*\n🌟 Rating: *{game[4]}*\n\n🌐 Website: *{game[5]}*'
    if(game[0] != 'No info'):
        bot.send_photo(clientId, photo="https:" + game[0], caption=sendText, parse_mode='Markdown', reply_markup = markupInline)
    else:
        bot.send_message(clientId, text=sendText, parse_mode= "Markdown", reply_markup = markupInline)

@bot.message_handler(commands = ['vrg'])
def VeryRandomGame(message):
    clientId = message.chat.id
    bot.send_message(clientId, text = "Your order in process! Wait a few second..", parse_mode = "Markdown")

    markupInline = types.InlineKeyboardMarkup()
    moreButton = types.InlineKeyboardButton("More..", callback_data="more_very_random_games")
    markupInline.add(moreButton)

    game = engine.FindRandomGame(True)
    sendText = f'🎮 Try play: *{game[1]}*\n\n🕹 Genres: *{game[2]}*\n\n📅 Release date: *{game[3]}*\n🌟 Rating: *{game[4]}*\n\n🌐 Website: *{game[5]}*'
    if(game[0] != 'No info'):
        bot.send_photo(clientId, photo="https:" + game[0], caption= sendText, parse_mode = 'Markdown', reply_markup = markupInline)
    else:
        bot.send_message(clientId, text=sendText, parse_mode= "Markdown", reply_markup = markupInline)

@bot.message_handler(commands = ['like'])
def SimillarGame(message):
    clientId = message.chat.id
    bot.send_message(clientId, text = "Your order in process! Wait a few second..", parse_mode = "Markdown")

    markupInline = types.InlineKeyboardMarkup()
    moreButton = types.InlineKeyboardButton("More..", callback_data="next_similar_game")
    markupInline.add(moreButton)

    gameName = message.text[6:]
    global similarGamesList
    similarGamesList = []
    game = ''

    if(gameName != ''):
        if similarGamesList == []:
            similarGamesList = engine.FindSimillarGame(gameName)
            game_id = random.randint(0, len(similarGamesList))
            game = engine.FindGamesById(similarGamesList.pop(game_id))
        else:
            game_id = random.randint(0, len(similarGamesList))
            game = engine.FindGamesById(similarGamesList.pop(game_id))
        if game != "None":
            sendText = f'🎮 Try play: *{game[1]}*\n\n🕹 Genres: *{game[2]}*\n\n📅 Release date: *{game[3]}*\n🌟 Rating: *{game[4]}*\n\n🌐 Website: *{game[5]}*'
            if(game[0] != 'No info'):
                bot.send_photo(clientId, photo="https:" + game[0], caption=sendText, parse_mode = 'Markdown', reply_markup = markupInline)
            else:
                bot.send_message(clientId, text=sendText, parse_mode="Markdown", reply_markup = markupInline)
        else:
            bot.send_message(clientId, text="Such a game does not exist or there is a mistake in writing!", parse_mode= "Markdown", reply_markup = markupInline)
    else:
        bot.send_message(clientId, text = 'There is no name of the game!')

def NextSimilarGame(message):
    clientId = message.chat.id
    bot.send_message(clientId, text = "Your order in process! Wait a few second..", parse_mode = "Markdown")

    markupInline = types.InlineKeyboardMarkup()
    moreButton = types.InlineKeyboardButton("More..", callback_data="next_similar_game")
    markupInline.add(moreButton)

    global similarGamesList
    game = ''
    if similarGamesList == []:
        bot.send_message(clientId, text = "Similar games are over!")
    else:
        game_id = random.randint(0, len(similarGamesList))
        game_id = similarGamesList.pop(game_id)
        game = engine.FindGamesById(game_id)
        sendText = f'🎮 Try play: *{game[1]}*\n\n🕹 Genres: *{game[2]}*\n\n📅 Release date: *{game[3]}*\n🌟 Rating: *{game[4]}*\n\n🌐 Website: *{game[5]}*'
        if(game[0] != 'No info'):
            bot.send_photo(clientId, photo="https:" + game[0], caption=sendText, parse_mode = 'Markdown', reply_markup = markupInline)
        else:
            bot.send_message(clientId, text=sendText, parse_mode="Markdown", reply_markup = markupInline)
    
@bot.callback_query_handler(func=lambda call: True)
def CallbackInline(call):
    if call.message:
        if call.data == "more_random_games":
            RandomGame(call.message)
        elif call.data == "more_very_random_games":
            VeryRandomGame(call.message)
        elif call.data == "next_similar_game":
            NextSimilarGame(call.message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
