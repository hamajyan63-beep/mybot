import telebot
import requests
import google.generativeai as genai
import re

# زانیارییە نوێیەکان
TOKEN = '8136305390:AAFm5OaVXYTk3UCan5l1ZzKoZYoHQH4tf0Y'
GEMINI_KEY = 'AIzaSyD0QMwRTIbSWGF8qnfE0AEsS1mK2tGKj4s'

bot = telebot.TeleBot(TOKEN)

# ڕێکخستنی مۆدێلی Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(func=lambda m: True)
def handle_all(m):
    # پشکنینی لینکی تیکتۆک
    if "tiktok.com" in m.text:
        bot.reply_to(m, "⏳ کەمێک چاوەڕێ بکە، خەریکم ڤیدیۆکە دایدەگرم...")
        try:
            links = re.findall(r'(https?://[^\s]+)', m.text)
            url = next((l for l in links if "tiktok.com" in l), m.text)
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            video_url = res['data']['play']
            bot.send_video(m.chat.id, video_url, caption="فەرموو براکەم ✨")
        except:
            bot.reply_to(m, "ببورە، کێشەیەک لە داگرتنی ڤیدیۆکە هەبوو.")
            
    # وەڵامدانەوە بە زمانی کوردی لە ڕێگەی زیرەکی دەستکردەوە
    else:
        try:
            bot.send_chat_action(m.chat.id, 'typing')
            # ڕێنمایی بۆ Gemini بۆ ئەوەی تەنها بە کوردی وەڵام بداتەوە
            prompt = f"وەک شارەزایەک تەنها بە زمانی کوردی سۆرانی وەڵامی ئەمە بدەرەوە: {m.text}"
            response = model.generate_content(prompt)
            bot.reply_to(m, response.text)
        except Exception as e:
            # ئەگەر هەر کێشەیەک هەبوو لێرە دەردەکەوێت
            print(f"Error: {e}")
            bot.reply_to(m, "ببورە، زیرەکی دەستکرد لەم کاتەدا وەڵامی نییە. کەمێکی تر تاقی بکەرەوە.")

if __name__ == "__main__":
    print("بۆتەکە بە کلیلە نوێیەکە دەستی پێکرد...")
    bot.polling(none_stop=True)
