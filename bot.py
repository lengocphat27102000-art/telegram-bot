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
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("8293088764:AAGS1gqgrL8M4Hfrdn1zpbpm3l1MAntBP6o")
CHANNEL_ID = os.getenv("-1003648760665")  # dạng: -100xxxxxxxxxx
WEBHOOK_URL = os.getenv("https://telegram-bot-miyz.onrender.com/webhook")  # https://ten-app.onrender.com/webhook
PORT = int(os.getenv("PORT", 10000))

# ================== LOG ==================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ================== TELEGRAM APP ==================
application = Application.builder().token(BOT_TOKEN).build()

# ================== FLASK ==================
app = Flask(__name__)

# ================== COMMANDS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot chứng khoán đã hoạt động!\n"
        "• Gõ tin nhắn để trao đổi\n"
        "• /post <nội dung> → gửi lên channel\n"
        "• /market → nhận định thị trường\n"
        "• /help → hướng dẫn"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 LỆNH BOT:\n"
        "/post <nội dung> – đăng lên channel\n"
        "/market – nhận định thị trường\n"
        "/time – xem thời gian hệ thống"
    )

async def post_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Dùng: /post nội dung")
        return

    content = " ".join(context.args)
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"📢 *BẢN TIN TỪ BOT*\n\n{content}",
        parse_mode="Markdown"
    )
    await update.message.reply_text("✅ Đã đăng lên channel")

async def market_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📊 *NHẬN ĐỊNH THỊ TRƯỜNG*\n\n"
        "• Xu hướng: TÍCH LŨY / TĂNG NHẸ\n"
        "• Dòng tiền: LUÂN CHUYỂN\n"
        "• Chiến lược: QUẢN TRỊ RỦI RO\n\n"
        "_(Có thể nâng cấp AI sau)_"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def time_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    await update.message.reply_text(f"⏰ Thời gian server: {now}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Bạn vừa gửi: {update.message.text}")

# ================== AUTO JOB ==================
async def auto_market_news():
    text = (
        "📈 *AUTO BẢN TIN THỊ TRƯỜNG*\n\n"
        "• VNINDEX: theo dõi vùng hỗ trợ\n"
        "• Nhóm CP mạnh: Ngân hàng – Chứng khoán\n"
        "• Khuyến nghị: Không FOMO"
    )
    await application.bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        parse_mode="Markdown"
    )

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Ho_Chi_Minh")
    scheduler.add_job(
        lambda: application.create_task(auto_market_news()),
        trigger="cron",
        hour=8,
        minute=30,
    )
    scheduler.start()

# ================== WEBHOOK ==================
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# ================== MAIN ==================
async def setup_bot():
    await application.initialize()
    await application.bot.set_webhook(WEBHOOK_URL)
    start_scheduler()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_cmd))
application.add_handler(CommandHandler("post", post_channel))
application.add_handler(CommandHandler("market", market_view))
application.add_handler(CommandHandler("time", time_cmd))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(setup_bot())
    app.run(host="0.0.0.0", port=PORT)
