import telebot
import requests
import re
import os

# زانیارییەکان
TOKEN = '8136305390:AAFm5OaVXYTk3UCan5l1ZzKoZYoHQH4tf0Y'
CH_ID = '@kurdmodhack' 
ADMIN_ID = 6185854746 

bot = telebot.TeleBot(TOKEN)

# فەنکشن بۆ زانیاری ئەندامانی چەناڵ
def get_channel_members():
    try:
        count = bot.get_chat_members_count(CH_ID)
        return count
    except:
        return "نادیار"

# پشکنینی جۆینی ناچاری
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
    # پشکنینی جۆین - کەسەکە تا جۆین نەبێت بۆتەکە کار ناکات
    if not check_join(m.from_user.id):
        bot.reply_to(m, f"🌟 سڵاو بەڕێزم،\nبۆ بەکارهێنانی بۆتەکە، تکایە سەرەتا جۆینی چەناڵی بەڕێز ئەسڵام بکە:\n\n👉 {CH_ID}")
        return

    member_count = get_channel_members()
    footer = f"\n\n📢 ژمارەی ئەندامانی چەناڵ: {member_count}"

    # ١. وەڵامدانەوەی سڵاو بەو شێوەیەی داوات کردبوو
    if m.text.lower() in ["سڵاو", "سلاو", "slaw", "hello"]:
        bot.reply_to(m, "سڵاو، کاتت باش. من دەتوانم یارمەتیت بدەم لە داگرتنی ڤیدیۆ بێ هیچ لۆگۆیەک. تەنها لینکەکە بنێرە! ✨" + footer)
        return

    # ٢. داگرتنی ڤیدیۆی تیکتۆک
    if "tiktok.com" in m.text:
        bot.reply_to(m, "⏳ کەمێک چاوەڕێ بکە، خەریکم ڤیدیۆکە ئامادە دەکەم...")
        try:
            # بەکارهێنانی API بۆ داگرتنی ڤیدیۆ بێ لۆگۆ
            res = requests.get(f"https://www.tikwm.com/api/?url={m.text}").json()
            video_url = res['data']['play']
            bot.send_video(m.chat.id, video_url, caption="فەرموو ڤیدیۆکەت بەبێ لۆگۆ ئامادەیە ✨" + footer)
        except:
            bot.reply_to(m, "ببورە، کێشەیەک لە داگرتنی ئەم لینکەدا هەبوو. دڵنیابە کە لینکەکە ڕاستە.")
    
    # ٣. ئەگەر شتێکی تری نووسی و لینک نەبوو
    else:
        bot.reply_to(m, "تکایە تەنها لینکی تیکتۆک بنێرە بۆ داگرتن، یان بڵێ 'سڵاو' بۆ زانیاری زیاتر. 😊" + footer)

if __name__ == "__main__":
    print("بۆتەکە بەبێ زیرەکی دەستکرد چالاک بوو...")
    bot.polling(none_stop=True)
