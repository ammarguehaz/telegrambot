import telegram
from telegram.ext import Updater, CommandHandler
import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime, timedelta

# Telegram Bot Token
TOKEN = 6102160876:AAGXCduDUD-YY71FxHxuTxgFUsUquS4lShg

# YouTube playlist URL containing the dars videos
YOUTUBE_PLAYLIST_URL = https://youtube.com/playlist?list=PL3a9QLvIi6XOL9bnmSu9I2h0TyelJn7Wi

# List of user feedback
feedback_list = []

# Create a Telegram bot instance
bot = telegram.Bot(token=TOKEN)

# Function to send a daily reminder to users
def send_daily_reminder(context):
    chat_ids = context.job.context
    dars = get_random_dars()
    message = f"📚 Daily Reminder: Here's the Dars of the Day\n\nTitle: {dars['title']}\n\nDescription: {dars['description']}\n\nListen on YouTube: {dars['youtube_url']}"
    for chat_id in chat_ids:
        bot.send_message(chat_id=chat_id, text=message)

# Command handler for /start command
def start(update, context):
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text="Welcome to the Cheikh Douros Bot! 🕌\n\nType /dars to receive a daily Dars reminder.")

# Command handler for /dars command
def dars(update, context):
    chat_id = update.effective_chat.id
    dars = get_random_dars()
    message = f"Dars of the Day\n\nTitle: {dars['title']}\n\nDescription: {dars['description']}\n\nListen on YouTube: {dars['youtube_url']}\n\nOr\n\nListen as Voice Message: /voice"
    bot.send_message(chat_id=chat_id, text=message)

# Command handler for /voice command
def voice(update, context):
    chat_id = update.effective_chat.id
    dars = get_random_dars()
    voice_file = fetch_voice_file(dars['youtube_url'])
    bot.send_voice(chat_id=chat_id, voice=open(voice_file, 'rb'))

# Command handler for /feedback command
def feedback(update, context):
    chat_id = update.effective_chat.id
    message = update.message.text.replace('/feedback', '').strip()
    if message:
        feedback_list.append(message)
        bot.send_message(chat_id=chat_id, text="Thank you for your feedback! 🙏")
    else:
        bot.send_message(chat_id=chat_id, text="Please provide your feedback after the /feedback command.")

# Function to scrape YouTube playlist and retrieve a random Dars
def get_random_dars():
    page = requests.get(YOUTUBE_PLAYLIST_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    videos = soup.find_all('a', {'class': 'yt-simple-endpoint inline-block style-scope ytd-playlist-video-renderer'})
    video = random.choice(videos)
    title = video['title']
    video_id = video['href'].replace('/watch?v=', '')
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    description = video.next_sibling.next_sibling.text.strip()
    return {'title': title, 'description': description, 'youtube_url': youtube_url}

# Function to fetch the voice file from YouTube video URL
def fetch_voice_file(youtube_url):
    # Implement your logic to convert the YouTube video to a voice file
    # and return the file path
    return 'path/to/voice/file.ogg'

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Command handlers
    start_handler = CommandHandler('start', start)
    dars_handler = CommandHandler('dars', dars)
    voice_handler = CommandHandler('voice', voice)
    feedback_handler = CommandHandler('feedback', feedback)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(dars_handler)
    dispatcher.add_handler(voice_handler)
    dispatcher.add_handler(feedback_handler)

    # Schedule daily reminder job
    job_queue = updater.job_queue
    reminder_time = datetime.now().replace(hour=8, minute=0, second=0)  # Set the desired time for the reminder
    chat_ids = [YOUR_CHAT_ID]  # Add the chat IDs of the users you want to send the daily reminder to
    job_queue.run_daily(send_daily_reminder, reminder_time, days=(0, 1, 2, 3, 4, 5, 6), context=chat_ids)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

