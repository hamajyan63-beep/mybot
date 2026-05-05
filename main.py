import telebot
import requests
import os

# زانیارییەکان
TOKEN = '8136305390:AAFm5OaVXYTk3UCan5l1ZzKoZYoHQH4tf0Y'
CH_ID = '@Saratayak' 
ADMIN_ID = 6185854746 

bot = telebot.TeleBot(TOKEN)
USER_FILE = "users_list.txt"

def update_bot_description(user_id):
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f: f.write("")
    with open(USER_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USER_FILE, "a") as f:
            f.write(f"{user_id}\n")
        count = len(users) + 1
        try:
            bot.set_my_description(f"🤖 بۆتی داگرتنی ڤیدیۆ بێ لۆگۆ\n👥 بەکارهێنەران: {count}\n📢 چەناڵ: {CH_ID}")
        except: pass

def get_bot_users_count():
    try:
        with open(USER_FILE, "r") as f: return len(f.readlines())
    except: return 0

def check_join(user_id):
    try:
        res = bot.get_chat_member(CH_ID, user_id)
        return res.status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(func=lambda m: True)
def handle_all(m):
    update_bot_description(m.from_user.id)
    
    # جۆینی ناچاری
    if not check_join(m.from_user.id):
        bot.reply_to(m, f"🌟 سڵاو بەڕێزم،\nبۆ بەکارهێنانی بۆتەکە، تکایە سەرەتا جۆینی چەناڵەکەمان بکە:\n\n👉 {CH_ID}")
        return

    bot_users = get_bot_users_count()
    footer = f"\n\n👥 بەکارهێنەرانی بۆت: {bot_users}\n📢 {CH_ID}"

    # ١. وەڵامی سڵاو
    if m.text.lower() in ["سڵاو", "سلاو", "slaw"]:
        bot.reply_to(m, "سڵاو، کاتت باش. تەنها لینکی ڤیدیۆی تیکتۆک بنێرە تا بەبێ لۆگۆ بۆت دابگرم! ✨" + footer)
    
    # ٢. داگرتنی تیکتۆک (تەنها ئەمە ماوەتەوە)
    elif "tiktok.com" in m.text:
        bot.reply_to(m, "⏳ کەمێک چاوەڕێ بکە...")
        try:
            res = requests.get(f"https://www.tikwm.com/api/?url={m.text}").json()
            bot.send_video(m.chat.id, res['data']['play'], caption="فەرموو پێشکەشە ✨" + footer)
        except:
            bot.reply_to(m, "❌ کێشەیەک لە داگرتنی ڤیدیۆکەدا هەبوو.")
            
    # ٣. ئەگەر هەر شتێکی تری نارد
    else:
        bot.reply_to(m, "تکایە تەنها لینکی تیکتۆک بنێرە. 😊" + footer)

if __name__ == "__main__":
    bot.polling(none_stop=True)
