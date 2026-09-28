import os
import json
from pathlib import Path
import telebot

TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)

DATA_FILE = Path("data.json")

def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"lesson": None, "students": {}}

def save_data():
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

data = load_data()

def student(message):
    uid = str(message.from_user.id)
    name = message.from_user.first_name or "بدون نام"

    if uid not in data["students"]:
        data["students"][uid] = {
            "name": name,
            "photo": False,
            "voice": False,
            "kahoot": False
        }
    else:
        data["students"][uid]["name"] = name

    return data["students"][uid]

@bot.message_handler(commands=["lesson"])
def new_lesson(message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        bot.reply_to(message, "مثال: /lesson 23")
        return

    data["lesson"] = parts[1]

    for s in data["students"].values():
        s["photo"] = False
        s["voice"] = False
        s["kahoot"] = False

    save_data()
    bot.reply_to(message, f"📚 درس {data['lesson']} شروع شد.")

@bot.message_handler(content_types=["photo"])
def photo_received(message):
    s = student(message)
    s["photo"] = True
    save_data()
    bot.reply_to(message, "📷 کارخانگی ✅")

@bot.message_handler(content_types=["voice"])
def voice_received(message):
    s = student(message)
    s["voice"] = True
    save_data()
    bot.reply_to(message, "🎙 ویس ✅")

@bot.message_handler(commands=["kahoot"])
def kahoot_done(message):
    s = student(message)
    s["kahoot"] = True
    save_data()
    bot.reply_to(message, "🎮 Kahoot ✅")

@bot.message_handler(commands=["status"])
def status(message):
    lesson = data.get("lesson") or "؟"

    if not data["students"]:
        bot.reply_to(message, "هنوز فعالیتی ثبت نشده.")
        return

    lines = [f"📚 درس {lesson}\n"]

    for s in data["students"].values():
        p = "✅" if s["photo"] else ""
        v = "✅" if s["voice"] else ""
        k = "✅" if s["kahoot"] else ""

        lines.append(
            f"{s['name']}: 📷{p}  🎙{v}  🎮{k}"
        )

    bot.reply_to(message, "\n".join(lines))

print("Bot is running...")
bot.infinity_polling(skip_pending=True)
