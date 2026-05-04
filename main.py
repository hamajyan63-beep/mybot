
import telebot
import requests

TOKEN = '8136305390:AAEukt2bvYpN6o9vthkesMeZ9LVzJBGA3Jo'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def handle(m):
    if "tiktok.com" in m.text:
        bot.reply_to(m, "⏳ کەمێک چاوەڕێ بکە...")
        try:
            # لێرە لینکەکە چاک دەکەین بۆ ئەوەی تەنها یوئار ئێڵەکە بێت
            url = m.text.split(" ")[0]
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            video_url = res['data']['play']
            bot.send_video(m.chat.id, video_url, caption="فەرموو براکەم ✨")
        except Exception as e:
            bot.reply_to(m, "ببورە، کێشەیەک لە داگرتنی ڤیدیۆکە هەبوو.")
    else:
        bot.reply_to(m, "سڵاو! تەنها لینکی تیکتۆکم بۆ بنێرە.")

bot.polling(none_stop=True)
