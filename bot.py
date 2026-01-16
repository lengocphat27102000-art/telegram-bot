from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = "8293088764:AAGS1gqgrL8M4Hfrdn1zpbpm3l1MAntBP6o"
CHANNEL_ID = -1003648760665

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot channel sẵn sàng hoạt động")

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Dùng: /post nội dung")
        return

    text = " ".join(context.args)

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=text
    )

    await update.message.reply_text("✅ Đã đăng lên channel")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post))

    print("🚀 Bot channel đang chạy...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()