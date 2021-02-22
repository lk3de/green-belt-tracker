#!/usr/bin/env python3

import config
import logging
import locale
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import gpxpy
import geopy.distance


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
    context.bot.send_message(chat_id=update.effective_chat.id, text='Berechnung läuft...')

    # update to latest message object if it's a live location
    message = None
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    
    user_latitude = message.location.latitude
    user_longitude = message.location.longitude
    logging.info('Incoming location with Latitude: {:.2f}, Longitude: {:.2f}'.format(user_latitude, user_longitude))

    #context.bot.send_message(chat_id=update.effective_chat.id, text='Deine Position ist (lat/lon): %.6f / %.6f' % (user_latitude, user_longitude))
    gpx_file = open(config.gpx_file, 'r')
    gpx = gpxpy.parse(gpx_file)

    
    # iterate through GPX and find the track point with shortest distance to user location
    closest = {'value': None, 'index': None}
    i = 0
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                point_distance = geopy.distance.distance((user_latitude, user_longitude), (point.latitude, point.longitude)).meters
                if closest['value'] == None:
                        closest['value'] = point_distance
                        closest['index'] = i
                elif point_distance < closest['value']:
                    closest['value'] = point_distance
                    closest['index'] = i
                i += 1
    
    distance = closest['value']
    percent = closest['index'] / i * 100

    logging.info('Distance is {:.2f}, percent finished is {:.2f}'.format(distance, percent))
    
    if distance < config.max_distance_meter:
        text = 'Du bist {:.2f}m vom grünen Band entfernt und hast schon {:.2f}% geschafft!'.format(distance, percent)
    else:
        text = 'Du bist weiter als {:.0f}m vom grünen Band entfernt ({:.2f}m). Berechnung nicht möglich!'.format(config.max_distance_meter, distance)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)




def main():

    # define logging format
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=config.log_level)

    # setting locale
    locale.setlocale(locale.LC_ALL, '')

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
    updater.start_polling()


if __name__ == '__main__':
    main()