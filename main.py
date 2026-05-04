import telebot
import requests
import re

TOKEN = '8136305390:AAEukt2bvYpN6o9vthkesMeZ9LVzJBGA3Jo'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def handle(m):
    # لێرە تەنها لینکەکە لە ناو دەقەکە دەردەهێنین
    links = re.findall(r'(https?://[^\s]+)', m.text)
    tiktok_link = next((l for l in links if "tiktok.com" in l), None)

    if tiktok_link:
        bot.reply_to(m, "⏳ کەمێک چاوەڕێ بکە...")
        try:
            res = requests.get(f"https://www.tikwm.com/api/?url={tiktok_link}").json()
            video_url = res['data']['play']
            bot.send_video(m.chat.id, video_url, caption="فەرموو براکەم ✨")
        except:
            bot.reply_to(m, "ببورە، کێشەیەک لە داگرتنی ڤیدیۆکە هەبوو.")
    else:
        bot.reply_to(m, "سڵاو! تەنها لینکی تیکتۆکم بۆ بنێرە.")

bot.polling(none_stop=True)
