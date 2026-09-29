import os
import telebot

TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["test"])
def test(message):
    bot.reply_to(message, "✅ بوت کار می‌کند")

@bot.message_handler(content_types=["photo"])
def photo(message):
    bot.reply_to(message, "📷 کارخانگی ✅")

@bot.message_handler(content_types=["voice"])
def voice(message):
    bot.reply_to(message, "🎙 ویس ✅")

print("Bot started")
bot.infinity_polling(skip_pending=True)
