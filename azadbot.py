from telegram.ext import Updater, CallbackContext, CommandHandler, \
	MessageHandler, filters, Application
from telegram import KeyboardButton, ReplyKeyboardMarkup
from decouple import config
from requests import *
from anon import Anon


API_TOKEN = config("API_TOKEN")
COMMANDS = (CMD_JOIN, CMD_SIKTIR, ) = ('{Join}', '{Siktir}',)
menu_main = [[KeyboardButton(CMD_JOIN), KeyboardButton(CMD_SIKTIR)]]


async def cmd_start(update: Updater, context: CallbackContext):
	anon = Anon.Get(update.message)
	
	await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hey {anon.id};", \
		reply_markup=ReplyKeyboardMarkup(menu_main, resize_keyboard=True, \
		one_time_keyboard=True))


async def cmd_join(update: Updater, context: CallbackContext):
	await update.message.reply_text('...')
	anon = Anon.Get(update.message)
	anon.next()
	if anon.companion:
		await update.message.reply_text(\
			f"Connected to {anon.companion.alias}:")
		await context.bot.send_message(chat_id=anon.companion.user_id, \
			text=f'Connected to {anon.alias}:')


async def cmd_siktir(update: Updater, context: CallbackContext):
	user = update.message.from_user
	if  user.id in Anon.Onlines:
		# handle companionship
		del Anon.Onlines[user.id]
	await update.message.reply_text('Siktir babe!')


async def broadcast(update: Updater, context: CallbackContext):
	chat = update.message.chat
	text = f'{chat.full_name}: {update.message.text}'
	for chat_id in Anon.Onlines:
		if chat_id != chat.id:
			await context.bot.send_message(chat_id, \
					text=text)

async def handle_messages(update:Updater, context: CallbackContext):
	text = update.message.text
	if text == CMD_JOIN:
		await cmd_join(update, context)

	elif text == CMD_SIKTIR:
		await cmd_siktir(update, context)
	else:
#		await broadcast(update, context)
		anon = Anon.Get(update.message)
		if anon and anon.companion:
			await context.bot.send_message(chat_id=anon.companion.user_id, \
				text=text)

if __name__ == "__main__":
	app = Application.builder().token(API_TOKEN).build()
	app.add_handler(CommandHandler("start", cmd_start))
	app.add_handler(CommandHandler('join', cmd_join))
	app.add_handler(MessageHandler(filters.ALL, \
		handle_messages))
	print("azadbot server's up and running now..")
	app.run_polling(1.0)
