import asyncio
import websockets
import json
import os
from telegram import Bot
from telegram.constants import ParseMode
from datetime import datetime
import pytz

# مفاتيح البوت - باش نحطوهم في Railway بعد شوية
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
DERIV_API_TOKEN = os.environ.get('DERIV_API_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)

async def send_signal(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)
        print(f"Sent: {message}")
    except Exception as e:
        print(f"Error sending: {e}")

async def deriv_bot():
    uri = "wss://ws.binaryws.com/websockets/v3?app_id=1089"
    async with websockets.connect(uri) as websocket:
        # Authorize
        await websocket.send(json.dumps({"authorize": DERIV_API_TOKEN}))
        auth_response = await websocket.recv()
        print("Authorized:", auth_response)
        
        await send_signal("🤠 <b>Cowboy Bot Connected</b>\n✅ Ready for signals 24/7")
        
        # هنا تحط منطق الاستراتيجية متاعك
        # هذا مثال بسيط يبعث رسالة كل ساعة
        while True:
            tunis_time = datetime.now(pytz.timezone('Africa/Tunis')).strftime('%H:%M:%S')
            await send_signal(f"🔥 <b>Cowboy Signal Test</b>\n⏰ Time: {tunis_time}\n📈 R_100 CALL 5min")
            await asyncio.sleep(3600)  # كل ساعة

if __name__ == "__main__":
    asyncio.run(deriv_bot())
