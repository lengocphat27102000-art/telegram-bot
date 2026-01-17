import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from flask import Flask, request

# ================== ENV ==================
BOT_TOKEN = os.getenv("8293088764:AAGS1gqgrL8M4Hfrdn1zpbpm3l1MAntBP6o")
CHANNEL_ID = os.getenv("-1003648760665")  # ví dụ: -100xxxxxxxxxx
WEBHOOK_URL = os.getenv("https://telegram-bot-1-lbep.onrender.com")  # https://ten-app.onrender.com/webhook
PORT = int(os.environ.get("PORT", 10000))

# ================== TELEGRAM APP ==================
application = Application.builder().token(BOT_TOKEN).build()

# ================== FLASK APP ==================
app = Flask(__name__)

# ================== HANDLERS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot chứng khoán đã sẵn sàng!\n"
        "• /post <nội dung> → đăng lên channel\n"
        "• Gõ tin nhắn → bot phản hồi"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📩 Bạn vừa gửi: {update.message.text}")

async def post_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Dùng: /post <nội dung>")
        return

    content = " ".join(context.args)
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"📊 **BẢN TIN CHỨNG KHOÁN**\n\n{content}",
        parse_mode="Markdown"
    )
    await update.message.reply_text("✅ Đã đăng lên channel")

# ================== REGISTER HANDLERS ==================
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("post", post_to_channel))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ================== WEBHOOK ENDPOINT ==================
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# ================== MAIN ==================
if __name__ == "__main__":
    async def run():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL)
        await application.start()

    import asyncio
    asyncio.get_event_loop().create_task(run())

    app.run(host="0.0.0.0", port=PORT)
