from telethon import TelegramClient, events
import requests
import json

# 👉 O'zingizning ma'lumotlaringizni kiriting
api_id = input("api_id: ")  # <-- API_ID
api_hash = input("api_hash: ")
session_name = "malakgpt_userbot"

# 🔐 2 bosqichli parolni shu yerda kiritish uchun
def get_2fa_password():
    return input("🛡 2 bosqichli parolingizni kiriting: ")

# 📲 Telegram client sozlash
client = TelegramClient(session_name, api_id, api_hash)
client.parse_mode = 'html'
client.password_callback = get_2fa_password

# 🧠 MalakGPTga so‘rov yuborish funksiyasi
def ask_malak_gpt(query):
    url = "https://s1365.surkhandc.uz/ai/"
    data = {
        "query": query
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            print("📨 API javobi:", response.text)  # Debug uchun
            result = response.json()
            return result.get("answer", "❗ Javob topilmadi.")
        else:
            return f"❌ HTTP xato: {response.status_code}"
    except Exception as e:
        return f"❌ So‘rovda xatolik: {str(e)}"

# 💬 Foydalanuvchi .ai bilan yozganda ishlovchi handler
@client.on(events.NewMessage(pattern=r'^\.ai (.+)'))
async def handler(event):
    query = event.pattern_match.group(1)
    await event.reply("🧠 MalakGPTga yuborilmoqda...")
    response = ask_malak_gpt(query)
    await event.respond(response)

# ▶️ Botni ishga tushirish
print("🤖 MalakGPT UserBot ishga tushdi.")
client.start()
client.run_until_disconnected()
