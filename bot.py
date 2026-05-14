import telebot
import requests
import re

BOT_TOKEN = '8645229756:AAHNPj9vFS9Ui-ClwYtwmCT8980wn5G18K4'
FIREBASE_DB_URL = 'https://lala-29a05-default-rtdb.firebaseio.com/'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: message.reply_to_message is not None)
def handle_reply(message):
    # আপনার আইডি থেকে রিকোয়েস্ট এসেছে কি না চেক করা
    if str(message.from_user.id) != '6258563456':
        return

    reply_to = message.reply_to_message
    
    if reply_to.caption:
        # ক্যাপশনের ভেতর থেকে শুধু USER_ এবং সংখ্যার অংশটুকু খুঁজে বের করার সহজ নিয়ম
        match = re.search(r'USER_\d+', reply_to.caption)
        if match:
            user_id = match.group(0)
            admin_number = message.text.strip()
            
            # ফায়ারবেস ডাটাবেসে নম্বর পাঠানো
            firebase_url = f"{FIREBASE_DB_URL}replies/{user_id}.json"
            data = {"number": admin_number}
            
            response = requests.put(firebase_url, json=data)
            
            if response.status_code == 200:
                bot.reply_to(message, f"✅ সফলভাবে ইউজারের স্ক্রিনে নম্বর পাঠানো হয়েছে!\n🆔 আইডি: {user_id}\n📱 নম্বর: {admin_number}")
            else:
                bot.reply_to(message, "❌ ডাটাবেসে পাঠাতে সমস্যা হয়েছে।")
        else:
            bot.reply_to(message, "❌ মেসেজ ক্যাপশনে কোনো ইউজার আইডি পাওয়া যায়নি।")

print("বটটি সফলভাবে সচল হয়েছে...")
bot.infinity_polling()