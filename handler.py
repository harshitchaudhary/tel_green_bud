from telegram.ext import Updater, CommandHandler
import mysql.connector

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '592559771:AAEmxJftMbJYkMJ-Z_B_cwS2oRCyKVj2zg0'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'db_1807_tel'
DB_NAME = 'telegram_api'

tel_db = mysql.connector.connect(
		host=DB_HOST,
		user=DB_USER,
		passwd=DB_PASSWORD,
		database=DB_NAME
	)
dbCursor = tel_db.cursor()
	

updater = Updater(token=TOKEN)

dispatcher = updater.dispatcher

def start(bot, update):
	user_id=update.message.chat.id
	user_exist_query = "SELECT count(*) FROM users WHERE tel_user_id='"+str(user_id)+"'";
	dbCursor.execute(user_exist_query)
	users = dbCursor.fetchall()
	if users[0][0] == 0:
		user_query = "INSERT INTO user (tel_user_id) values('"+str(user_id)+"')"
	else:
		touchUser(user_id)
	bot.send_message(chat_id=update.message.chat_id, text="Welcome to Green Bud, Buddy for nature and plants. Type \'/actions\' to show what all you can do")


def subscribe(bot, update):
	user_id = update.message.chat.id
	subscribe_query = "UPDATE users set subscribed = 1 where tel_user_id = '"+str(user_id)+"'"
	dbCursor.execute(subscribe_query)
	bot.send_message(chat_id=update.message.chat_id, text= "Thank you for subscribing "+ update.message.chat.first_name + ". You can unsubscribe anytime by typing /unsubscribe")

def unsubscribe(bot, update):
	user_id = update.message.chat.id
        unsubscribe_query = "UPDATE users set subscribed = 0 where tel_user_id = '"+str(user_id)+"'"
        dbCursor.execute(unsubscribe_query)
        bot.send_message(chat_id=update.message.chat_id, text= "You have been unsubscribed successfully")

def showHandles(bot, update):
	handle_list_query = "SELECT * FROM tel_handlers limit 0, 5"
	dbCursor.execute(handle_list_query)
	handles = dbCursor.fetchall()
	handle_text = "";
	for handle in handles:
		handle_text += "/" + str(handle[1]) + "\n"

	bot.send_message(chat_id=update.message.chat_id, text=handle_text)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

subs_handler = CommandHandler('subscribe', subscribe)
dispatcher.add_handler(subs_handler)

unsub_handler = CommandHandler('unsubscribe', unsubscribe)
dispatcher.add_handler(unsub_handler)

action_handler = CommandHandler('actions', showHandles)
dispatcher.add_handler(action_handler)

def touchUser(user_id):
	return 0; 

updater.start_polling()
