import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# CONFIG – LẤY TỪ ENV
# =========================
BOT_TOKEN = os.getenv("8293088764:AAEtieskYMNNHcFLja2N9o0Y5kT7aJe5t8g")      # 🔴 BẮT BUỘC – token từ BotFather
CHANNEL_ID = os.getenv("-1003648760665")    # 🔴 BẮT BUỘC – dạng -100xxxxxxxxxx
WEBHOOK_URL = os.getenv("https://telegram-bot-miyz.onrender.com/webhook")  # 🔴 BẮT BUỘC – https://ten-app.onrender.com/webhook
PORT = int(os.getenv("PORT", 10000))    # Render tự set PORT

# =========================
# LOG
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# =========================
# TELEGRAM HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot chứng khoán đã hoạt động!\n\n"
        "📌 Lệnh hỗ trợ:\n"
        "/bangtin – Bảng tin thị trường\n"
        "/nhan_dinh – Nhận định thị trường\n"
        "/khuyen_nghi – Gửi khuyến nghị\n"
        "/post <nội dung> – Đăng lên channel"
    )

async def bang_tin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📊 **BẢNG TIN THỊ TRƯỜNG**\n\n"
        "• VNINDEX: cập nhật\n"
        "• Thanh khoản: cập nhật\n"
        "• Nhóm ngành nổi bật: cập nhật\n"
        "• Khối ngoại: cập nhật\n\n"
        "⏰ Nguồn: Bot MBS Trading Signal"
    )
    await update.message.reply_text(text)

async def nhan_dinh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📈 **NHẬN ĐỊNH THỊ TRƯỜNG**\n\n"
        "Thị trường đang trong giai đoạn tích lũy.\n"
        "Chiến lược: Quan sát – giải ngân thăm dò.\n\n"
        "⚠️ Quản trị rủi ro chặt chẽ."
    )
    await update.message.reply_text(text)

async def khuyen_nghi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💡 **KHUYẾN NGHỊ**\n\n"
        "• Cổ phiếu: ABC\n"
        "• Vùng mua: 20 – 21\n"
        "• Mục tiêu: 24\n"
        "• Cắt lỗ: 19\n\n"
        "📌 Lưu ý: Tham khảo – không phải khuyến nghị đầu tư."
    )
    await update.message.reply_text(text)

async def post_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Cú pháp: /post <nội dung>")
        return

    content = " ".join(context.args)
    await context.bot.send_message(chat_id=CHANNEL_ID, text=content)
    await update.message.reply_text("✅ Đã đăng lên channel")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📩 Bạn vừa gửi: {update.message.text}")

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
    return "Bot is running!"

# =========================
# MAIN
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

    logging.info("🚀 Bot started & webhook set")

if __name__ == "__main__":
    import asyncio
    asyncio.run(setup())
    app.run(host="0.0.0.0", port=PORT)
