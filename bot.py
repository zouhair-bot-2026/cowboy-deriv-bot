import asyncio 
import google.generativeai as genai 
from telegram import Bot 
import os 

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
CHAT_ID = os.getenv("CHAT_ID") 

genai.configure(api_key=GEMINI_API_KEY) 
model = genai.GenerativeModel('gemini-1.5-flash') 
bot = Bot(token=TELEGRAM_TOKEN) 

async def send_signal(): 
    prompt = """ انت محلل فني. حلل زوج EUR/USD على فريم 1 ساعة. ارجعلي جواب مختصر: BUY او SELL او WAIT فقط، ومعاها سبب في سطر واحد بالعربي. """ 
    response = model.generate_content(prompt) 
    message = f"📡 **إشارة Gemini AI**\n\n{response.text}" 
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown") 

async def main(): 
    while True: 
        await send_signal() 
        await asyncio.sleep(3600) # يبعث كل ساعة 

if __name__ == "__main__": 
    asyncio.run(main())