import telebot

API_TOKEN = '6473668158:AAGI-btt6VaDgOsaEiVLxQbVPVYQ0ErYfo8'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['get_channels'])
def get_channels(message):
    subscribed_channels = []

    try:
        # Get the list of chat IDs the user is a part of
        chat_ids = [chat.id for chat in bot.get_chat(message.from_user.id).chat_ids()]

        for chat_id in chat_ids:
            try:
                chat_member = bot.get_chat_member(chat_id, message.from_user.id)
                if chat_member.status in ('administrator', 'member'):
                    chat_info = bot.get_chat(chat_id)
                    subscribed_channels.append(chat_info.username)
            except Exception as e:
                print(f"Error checking channel {chat_id}: {e}")

        if subscribed_channels:
            bot.reply_to(message, f"Subscribed channels: {', '.join(subscribed_channels)}")
        else:
            bot.reply_to(message, "You are not a member of any channels.")
    except Exception as e:
        print(f"Error getting chat IDs: {e}")

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.reply_to(message, "Welcome! Use /get_channels to check subscribed channels.")

# Polling loop
bot.polling(none_stop=True)
