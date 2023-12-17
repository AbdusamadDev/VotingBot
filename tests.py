import telebot

API_TOKEN = '6473668158:AAGI-btt6VaDgOsaEiVLxQbVPVYQ0ErYfo8'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['get_channels'])
def get_channels(message):
    # Replace with the channel usernames you want to check
    channel_usernames = ['@LAYFXAK_KANAL', 'channel_username2']

    subscribed_channels = []

    for channel_username in channel_usernames:
        try:
            chat_member = bot.get_chat_member(f'@{channel_username}', message.from_user.id)
            if chat_member.status in ('administrator', 'member'):
                subscribed_channels.append(channel_username)
        except Exception as e:
            print(f"Error checking channel {channel_username}: {e}")

    bot.reply_to(message, f"Subscribed channels: {', '.join(subscribed_channels)}")

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.reply_to(message, "Welcome! Use /get_channels to check subscribed channels.")

# Polling loop
bot.polling(none_stop=True)
