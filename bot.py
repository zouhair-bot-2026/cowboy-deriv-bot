import asyncio
import os
import google.generativeai as genai
from telegram import Bot

# أسماء الـ Environment Variables لازم تطابق Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# تأكد انو القيم موجودة
if not TELEGRAM_TOKEN or not GEMINI_API_KEY or not CHAT_ID:
    raise ValueError("تأكد حطيت TELEGRAM_BOT_TOKEN, GEMINI_API_KEY, TELEGRAM_CHAT_ID في Render")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = Bot(token=TELEGRAM_TOKEN)

# الأزواج العشرة اللي قلتلي عليهم
PAIRS = [
    "EUR/USD",
    "GBP/USD", 
    "USD/JPY",
    "AUD/USD",
    "USD/CHF",
    "EUR/CHF",
    "EUR/GBP",
    "GBP/JPY",
    "USD/CAD",
    "NZD/USD"
]

async def send_signal(pair):
    prompt = f"""انت محلل فني. حلل زوج {pair} على فريم 1 ساعة. 
ارجعلي جواب مختصر: BUY او SELL او WAIT فقط، ومعاها سبب في سطر واحد بالعربي.
لا تضيف اي كلام زايد."""
    
    try:
        response = model.generate_content(prompt)
        message = f"📡 **إشارة Gemini AI**\n\n**{pair}**: {response.text}"
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
    except Exception as e:
        error_msg = f"❌ **Error**\n\n{pair}: {str(e)}"
        await bot.send_message(chat_id=CHAT_ID, text=error_msg)

async def main():
    while True:
        for pair in PAIRS:
            await send_signal(pair)
            await asyncio.sleep(5)  # استنى 5 ثواني بين كل زوج باش ما يبلعكش Telegram
        
        await asyncio.sleep(3600)  # يبعث كل ساعة

if __name__ == "__main__":
    asyncio.run(main())