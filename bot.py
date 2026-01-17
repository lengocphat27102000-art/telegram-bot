import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

# ===== ENV =====
BOT_TOKEN = os.getenv("8293088764:AAEUeKoWGUVhqXtTKRz1In_iMjk0JVKgGOo")
CHANNEL_ID = os.getenv("-1003648760665")
WEBHOOK_URL = os.getenv("https://telegram-bot-faj6.onrender.com/webhook")

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN is missing in Environment Variables")

# ===== BOT =====
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

application = Application.builder().token(BOT_TOKEN).build()

# ===== COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot chứng khoán đã hoạt động!\n"
        "Gõ /market để xem bảng tin\n"
        "Gõ /help để xem lệnh"
    )

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 BẢNG TIN THỊ TRƯỜNG\n"
        "- VNINDEX: 1.2xx\n"
        "- Thanh khoản: ...\n"
        "- Xu hướng: Sideway / Uptrend"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/market – Bảng tin\n"
        "/start – Khởi động bot\n"
        "/help – Trợ giúp"
    )

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("market", market))
application.add_handler(CommandHandler("help", help_cmd))

# ===== WEBHOOK =====
@app.route("/webhook", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Bot is running"

# ===== START =====
if __name__ == "__main__":
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=WEBHOOK_URL + "/webhook"
    )
