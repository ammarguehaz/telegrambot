import gspread
import time
import datetime
import telegram
from telegram.ext import CommandHandler, Updater

# Google Sheets API credentials
gc = gspread.service_account(filename='creds.json')
sheet_name = 'Sheet1'
worksheet = gc.open(sheet_name).sheet1

# Telegram Bot API credentials
bot_token = '6146583905:AAF0bdbG8AQFWd7pqbGagHKvh1QFq35eB6U'
chat_id = '1623438268'
bot = telegram.Bot(token=bot_token)

# Add command handler
def add(update, context):
    # Get current time and date
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get user name from update object
    user_name = update.message.from_user.username

    # Get message text from update object
    message_text = update.message.text

    # Split message text into words
    words = message_text.split()

    # Get values to add to sheet
    value1 = words[1]
    value2 = words[2]

    # Add values to sheet
    row = [current_time, user_name, value1, value2]
    worksheet.append_row(row)

    # Send confirmation message to user
    message = f'Values ({value1}, {value2}) added to sheet'
    bot.send_message(chat_id=chat_id, text=message)

# Remove command handler
def remove(update, context):
    # Get current time and date
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get user name from update object
    user_name = update.message.from_user.username

    # Get message text from update object
    message_text = update.message.text

    # Split message text into words
    words = message_text.split()

    # Get row number to remove from sheet
    row_number = int(words[1])

    # Remove row from sheet
    worksheet.delete_row(row_number)

    # Send confirmation message to user
    message = f'Row {row_number} removed from sheet'
    bot.send_message(chat_id=chat_id, text=message)

# Create bot and add command handlers
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('add', add))
dispatcher.add_handler(CommandHandler('remove', remove))

# Start bot
updater.start_polling()
updater.idle()

