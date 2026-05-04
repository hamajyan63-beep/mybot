import telebot
import requests
import re

TOKEN = '8136305390:AAFm5OaVXYTk3UCan5l1ZzKoZYoHQH4tf0Y'
CH_ID = '@kurdmodhack' 

bot = telebot.TeleBot(TOKEN)

def check_join(user_id):
    try:
        res = bot.get_chat_member(CH_ID, user_id)
        return res.status in ['member', 'administrator', 'creator']
    except: return True

@bot.message_handler(func=lambda m: True)
def handle_all(m):
    # جۆینی ناچاری (دەتوانی لایبەری ئەگەر نەتویست)
    if not check_join(m.from_user.id):
        bot.reply_to(m, f"🌟 سەرەتا جۆینی چەناڵی بەڕێز ئەسڵام بکە:\n\n👉 {CH_ID}")
        return

    # ١. داگرتنی پۆستی تێلیگرام (بەبێ سنووردارکردنی کات)
    if "t.me/" in m.text:
        bot.reply_to(m, "⏳ خەریکم ناوەڕۆکی پۆستەکە کۆپی دەکەم...")
        try:
            # پارچە پارە کردنی لینکەکە بۆ گەیشتن بە ئایدی پۆستەکە
            link_parts = m.text.replace('https://', '').split('/')
            
            # ئەگەر لینکی چەناڵی گشتی بێت (وەک t.me/channel/123)
            if len(link_parts) >= 3:
                chat_id = f"@{link_parts[1]}"
                msg_id = int(link_parts[2])
                
                # بەکارهێنانی copy_message بۆ تێپەڕاندنی قفڵی سکرین و فۆروارد
                bot.copy_message(m.chat.id, chat_id, msg_id)
            else:
                bot.reply_to(m, "❌ لینکی پۆستەکە ناتەواوە.")
        except Exception as e:
            bot.reply_to(m, "❌ کێشەیەک هەبوو: یان چەناڵەکە تایبەتە و بۆتەکە لێی نییە، یان لینکەکە هەڵەیە.")
        return

    # ٢. بەشی تیکتۆک (هەمیشە چالاکە)
    if "tiktok.com" in m.text:
        bot.reply_to(m, "⏳ خەریکم ڤیدیۆکەت بۆ ئامادە دەکەم...")
        try:
            res = requests.get(f"https://www.tikwm.com/api/?url={m.text}").json()
            bot.send_video(m.chat.id, res['data']['play'], caption="فەرموو بێ لۆگۆ ئامادەیە ✨")
        except:
            bot.reply_to(m, "❌ کێشەیەک لە داگرتنی تیکتۆکەکە هەبوو.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
