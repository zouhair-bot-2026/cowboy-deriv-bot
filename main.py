import asyncio
import os
from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime
import pytz

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = Bot(token=TELEGRAM_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤠 Cowboy Pocket Bot شغال\nاستعمل /signal باش تطلب إشارة")

async def send_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # هنا تحط منطق التحليل متاعك
    # توة نحط مثال يدوي
    tunis_time = datetime.now(pytz.timezone('Africa/Tunis')).strftime('%H:%M:%S')
    
    message = f"""
🔔 <b>Pocket Option Signal</b>

📈 الزوج: EUR/USD OTC
📊 الأمر: PUT هبوط  
⏱ المدة: 5 دقايق
⏰ الوقت: {tunis_time}
🎯 السبب: مقاومة 1.1630 + RSI نازل

⚠️ Demo فقط قبل الحقي
    """
    
    await context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)
    await update.message.reply_text("✅ الإشارة تبعثت للقناة")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", send_signal))
    
    print("Bot running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
