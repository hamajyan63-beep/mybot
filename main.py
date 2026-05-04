import telebot
import requests
import google.generativeai as genai
import re
import os

# زانیارییەکان
TOKEN = '8136305390:AAFm5OaVXYTk3UCan5l1ZzKoZYoHQH4tf0Y'
GEMINI_KEY = 'AIzaSyD0QMwRTIbSWGF8qnfE0AEsS1mK2tGKj4s'
CH_ID = '@kurdmodhack' 
ADMIN_ID = 6185854746 

bot = telebot.TeleBot(TOKEN)

# ڕێکخستنی Gemini بە فێڵێکی سادە بۆ تێپەڕاندنی بلۆکی ناوچە (وەک کارکردنی VPN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_channel_members():
    try:
        count = bot.get_chat_members_count(CH_ID)
        return count
    except:
        return "نادیار"

def check_join(user_id):
    try:
        res = bot.get_chat_member(CH_ID, user_id)
        if res.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return False

@bot.message_handler(func=lambda m: True)
def handle_all(m):
    # ١. جۆینی ناچاری (کەسەکە نەتوانێت هیچ بنووسێت تا جۆین نەبێت)
    if not check_join(m.from_user.id):
        bot.reply_to(m, f"🌟 سڵاو بەڕێزم،\nبۆ بەکارهێنانی بۆتەکە، تکایە سەرەتا جۆینی چەناڵی بەڕێز ئەسڵام بکە:\n\n👉 {CH_ID}")
        return

    member_count = get_channel_members()
    footer = f"\n\n📢 ژمارەی ئەندامانی چەناڵ: {member_count}"

    # ٢. بەشی تیکتۆک
    if "tiktok.com" in m.text:
        bot.reply_to(m, "⏳ کەمێک چاوەڕێ بکە...")
        try:
            links = re.findall(r'(https?://[^\s]+)', m.text)
            url = next((l for l in links if "tiktok.com" in l), m.text)
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            bot.send_video(m.chat.id, res['data']['play'], caption="فەرموو پێشکەشە ✨" + footer)
        except:
            bot.reply_to(m, "کێشەیەک لە لینکی تیکتۆکەکە هەیە.")
            
    # ٣. بەشی زیرەکی دەستکرد (بە فێڵی تێپەڕاندنی سێرڤەر)
    else:
        try:
            bot.send_chat_action(m.chat.id, 'typing')
            # لێرەدا فەرمانەکە کەمێک دەگۆڕین تاوەکو سێرڤەرەکە ناچار بێت وەڵام بداتەوە
            response = model.generate_content(
                f"تۆ یاریدەدەرێکی کوردی، بە کوردی سۆرانی وەڵام بدەرەوە: {m.text}",
                generation_config=genai.types.GenerationConfig(temperature=0.4)
            )
            bot.reply_to(m, response.text + footer)
        except Exception as e:
            # ئەگەر هەر ئیشی نەکرد، ئەم پەیامە دەدات
            bot.reply_to(m, "ببورە، زیرەکی دەستکردەکە هێشتا کێشەی ناوچەی هەیە لەسەر Railway.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
