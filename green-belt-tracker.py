#!/usr/bin/env python3

import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging


# function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Herzlich willkommen! Ich bin der Green Belt Tracker Bot.')


# function to handle the /help command
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Tut mir leid, ich habe keine Hilfe-Funktion implementiert.')


# function to handle normal text messages
def text(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Du hast gerade "{update.message.text}" geschrieben.')

# function to handle location messages
def location(update, context):
    #context.bot.send_message(chat_id=update.effective_chat.id, text='Danke für deinen Standort.')

    message = None
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    
    user_latitude = message.location.latitude
    user_longitude = message.location.longitude

    context.bot.send_message(chat_id=update.effective_chat.id, text='Deine Position ist (lat/lon): %.6f / %.6f' % (user_latitude, user_longitude))
    


def main():

    # define logging format
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=config.log_level)

    # create the updater, that will automatically create also a dispatcher and a queue to make them dialoge
    updater = Updater(token=config.bot_token)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler(command='start', filters=Filters.chat(chat_id=config.user_id_list), callback=start))
    dispatcher.add_handler(CommandHandler(command='help', callback=help))

    # add an handler for normal text messages
    dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=text))

    # add an handler for location messages
    dispatcher.add_handler(MessageHandler(filters=Filters.location, callback=location))

    # start the bot
    print('Press Ctrl-C to abort')
    updater.start_polling()


if __name__ == '__main__':
    main()