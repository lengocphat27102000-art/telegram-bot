import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from apscheduler.schedulers.background import BackgroundScheduler

# =========================
# ENV – BẮT BUỘC ĐIỀN TRÊN RENDER
# =========================
BOT_TOKEN = os.getenv("8293088764:AAEtieskYMNNHcFLja2N9o0Y5kT7aJe5t8g")        # token BotFather
CHANNEL_ID = os.getenv("-1003648760665")      # -100xxxxxxxxxx
WEBHOOK_URL = os.getenv("https://telegram-bot-miyz.onrender.com/webhook")    # https://ten-app.onrender.com/webhook
PORT = int(os.getenv("PORT", 10000))

logging.basicConfig(level=logging.INFO)

# =========================
# BOT COMMANDS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 BOT CHỨNG KHOÁN\n\n"
        "/bangtin – Bảng tin thị trường\n"
        "/nhan_dinh – Nhận định\n"
        "/khuyen_nghi – Khuyến nghị\n"
        "/post <nội dung> – Đăng channel"
    )
    await update.message.reply_text(text)

async def bang_tin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 BẢNG TIN THỊ TRƯỜNG\n"
        "• VNINDEX: cập nhật\n"
        "• Thanh khoản: cập nhật\n"
        "• Khối ngoại: cập nhật"
    )

async def nhan_dinh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 NHẬN ĐỊNH THỊ TRƯỜNG\n"
        "Xu hướng: Sideway\n"
        "Chiến lược: Quan sát – chọn lọc cổ phiếu"
    )

async def khuyen_nghi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💡 KHUYẾN NGHỊ\n"
        "CP: ABC\n"
        "Vùng mua: 20–21\n"
        "Target: 24\n"
        "Cắt lỗ: 19"
    )

async def post_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Cú pháp: /post <nội dung>")
        return

    message = " ".join(context.args)
    await context.bot.send_message(chat_id=CHANNEL_ID, text=message)
    await update.message.reply_text("✅ Đã đăng lên channel")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📩 Bạn gửi: {update.message.text}")

# =========================
# AUTO JOB
# =========================
def auto_bang_tin():
    asyncio.run(
        application.bot.send_message(
            chat_id=CHANNEL_ID,
            text="⏰ BẢNG TIN TỰ ĐỘNG\nVNINDEX – Thanh khoản – Nhóm ngành"
        )
    )

# =========================
# FLASK + WEBHOOK
# =========================
app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

@app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot is running"

# =========================
# START
# =========================
async def setup():
    await application.initialize()
    await application.bot.set_webhook(WEBHOOK_URL)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("bangtin", bang_tin))
    application.add_handler(CommandHandler("nhan_dinh", nhan_dinh))
    application.add_handler(CommandHandler("khuyen_nghi", khuyen_nghi))
    application.add_handler(CommandHandler("post", post_channel))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_bang_tin, "cron", hour=8, minute=30)
    scheduler.start()

    logging.info("🚀 Bot đã sẵn sàng")

if __name__ == "__main__":
    asyncio.run(setup())
    app.run(host="0.0.0.0", port=PORT)
