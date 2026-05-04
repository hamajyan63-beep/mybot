import telebot
import requests
import google.generativeai as genai
import re

# کلیلەکان بە ڕاستەوخۆ لێرە بنووسە
TOKEN = '8136305390:AAFm5OaVXYTk3UCan5l1ZzKoZYoHQH4tf0Y'
GEMINI_KEY = 'AIzaSyCfkobBQIcvMEZxyDYKuR7DPtk9s9rQvss'

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(func=lambda m: True)
def handle_all(m):
    if "tiktok.com" in m.text:
        bot.reply_to(m, "⏳ کەمێک چاوەڕێ بکە...")
        try:
            links = re.findall(r'(https?://[^\s]+)', m.text)
            url = next((l for l in links if "tiktok.com" in l), m.text)
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            bot.send_video(m.chat.id, res['data']['play'], caption="فەرموو ✨")
        except:
            bot.reply_to(m, "کێشەیەک لە تیکتۆک هەیە.")
    else:
        try:
            bot.send_chat_action(m.chat.id, 'typing')
            prompt = f"وەک یاریدەدەرێکی زیرەک، تەنها بە زمانی کوردی سۆرانی وەڵامی ئەمە بدەرەوە: {m.text}"
            response = model.generate_content(prompt)
            bot.reply_to(m, response.text)
        except:
            bot.reply_to(m, "ببورە، زیرەکی دەستکرد کەمێک ماندووە.")

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
