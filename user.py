from telethon import TelegramClient, events
import requests
import json

# 👉 Fayllardan API_ID va API_HASH ni o'qish
with open("api.txt", "r") as f:
    api_id = int(f.read().strip())

with open("hash.txt", "r") as f:
    api_hash = f.read().strip()

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
            return result.get("response", "❗ Javob topilmadi.")  # <-- to‘g‘ri kalit nomi
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
