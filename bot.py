import os
import asyncio
from datetime import time
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
CHANNEL_ID = os.getenv("-1003648760665")
WEBHOOK_URL = os.getenv("https://telegram-bot-1-lbep.onrender.com")
PORT = int(os.environ.get("PORT", 10000))

# ================== TELEGRAM ==================
application = Application.builder().token(BOT_TOKEN).build()

# ================== FLASK ==================
app = Flask(__name__)

# ================== BASIC ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 BOT CHỨNG KHOÁN\n\n"
        "Lệnh khả dụng:\n"
        "/post <nội dung> – Đăng lên channel\n"
        "/signal – Gửi khuyến nghị mẫu\n"
        "/news – Gửi bản tin nhanh\n"
        "/view – Nhận định thị trường\n"
    )

# ================== POST TAY ==================
async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ /post <nội dung>")
        return

    content = " ".join(context.args)
    await context.bot.send_message(chat_id=CHANNEL_ID, text=content)
    await update.message.reply_text("✅ Đã đăng channel")

# ================== MỤC 1: BẢN TIN SÁNG ==================
async def morning_news(context: ContextTypes.DEFAULT_TYPE):
    message = (
        "📊 *BẢN TIN THỊ TRƯỜNG SÁNG*\n\n"
        "📌 *VN-Index*\n"
        "– Xu hướng: Sideway tăng\n"
        "– Hỗ trợ: 1240\n"
        "– Kháng cự: 1260\n\n"
        "💰 *Dòng tiền*\n"
        "– Ngân hàng: Trung tính\n"
        "– Chứng khoán: Tích cực\n"
        "– BĐS: Phân hóa\n\n"
        "📈 *Chiến lược*\n"
        "– Giữ tỷ trọng 50–60%\n"
        "– Ưu tiên cổ phiếu nền tích lũy\n\n"
        "#BanTinSang #ThiTruong"
    )

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode="Markdown"
    )

# ================== MỤC 2: KHUYẾN NGHỊ ==================
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "📌 *KHUYẾN NGHỊ GIAO DỊCH*\n\n"
        "• Mã: ABC\n"
        "• Vùng mua: 20 – 21\n"
        "• Mục tiêu: 24\n"
        "• Cắt lỗ: 19\n"
        "• Tỷ trọng: 10–15%\n\n"
        "⚠️ Tham khảo – tự chịu trách nhiệm"
    )

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode="Markdown"
    )
    await update.message.reply_text("✅ Đã gửi khuyến nghị")

# ================== MỤC 3: NHẬN ĐỊNH ==================
async def view_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "📈 *NHẬN ĐỊNH THỊ TRƯỜNG*\n\n"
        "• Xu hướng ngắn hạn: Trung tính\n"
        "• Dòng tiền: Luân chuyển\n"
        "• Rủi ro: Áp lực chốt lời cuối phiên\n\n"
        "Chiến lược:\n"
        "– Không mua đuổi\n"
        "– Ưu tiên cổ phiếu mạnh hơn thị trường"
    )

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode="Markdown"
    )
    await update.message.reply_text("✅ Đã gửi nhận định")

# ================== MỤC 4: TIN TỨC ==================
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "📰 *TIN TỨC NỔI BẬT*\n\n"
        "• FED giữ nguyên lãi suất\n"
        "• Khối ngoại quay lại mua ròng\n"
        "• Nhóm ngân hàng hút dòng tiền\n\n"
        "#TinTuc #ChungKhoan"
    )

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode="Markdown"
    )
    await update.message.reply_text("✅ Đã gửi tin tức")

# ================== REGISTER ==================
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("post", post))
application.add_handler(CommandHandler("signal", signal))
application.add_handler(CommandHandler("view", view_market))
application.add_handler(CommandHandler("news", news))

# ================== WEBHOOK ==================
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

        # ⏰ Bản tin sáng 08:30
        application.job_queue.run_daily(
            morning_news,
            time=time(hour=8, minute=30)
        )

    asyncio.get_event_loop().create_task(run())
    app.run(host="0.0.0.0", port=PORT)
