# Settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai
import json
import argparse
import sys

# Parse args
parser = argparse.ArgumentParser(description="standalone parser")
parser.add_argument('--token_tel', dest='token_tel')
parser.add_argument('--token_dialog', dest='token_dialog')
parser.add_argument('--id_dialog', dest='id_dialog')
args, sys.argv[1:] = parser.parse_known_args(sys.argv[1:])

# Token API to Telegram
updater = Updater(token=args.token_tel)
dispatcher = updater.dispatcher


# Command processing
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


def textMessage(bot, update):
    request = apiai.ApiAI(args.token_dialog).text_request()  # Token API to Dialogflow
    request.lang = 'ru'  # In which language will the request be sent
    request.session_id = args.id_dialog  # ID Sessions of the dialogue (you need to then learn the bot)
    request.query = update.message.text  # We send a request to the AI with a message from the user
    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech']  # Disassemble JSON and pull out the answer

    # If there is an answer from the bot - we send to the user, if not - the bot did not understand it
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')


# Handlers
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

# add handlers to the dispatcher
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

# Getting Started for Updates
updater.start_polling(clean=True)

# Stop the bot if Ctrl + C was pressed
updater.idle()
