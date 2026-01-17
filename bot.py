import os
import requests
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

# =====================
# ENVIRONMENT VARIABLES
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not BOT_TOKEN or not WEBHOOK_URL:
    raise RuntimeError("❌ BOT_TOKEN hoặc WEBHOOK_URL chưa được cấu hình")

# =====================
# FASTAPI APP
# =====================
app = FastAPI()

tg_app = Application.builder().token(BOT_TOKEN).build()

# =====================
# COMMAND HANDLERS
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Bot Chứng Khoán Việt Nam\n"
        "Gõ /market để xem thông tin thị trường"
    )

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Demo dữ liệu thị trường VN
    (có thể thay API thật sau)
    """
    data = get_vn_market_news()
    await update.message.reply_text(data)

def get_vn_market_news():
    # Demo – sau này bạn thay API thật
    return (
        "📈 Thị trường chứng khoán VN\n"
        "- VNINDEX: 1,180 (+5.2)\n"
        "- Thanh khoản: 18,000 tỷ\n"
        "- Nhóm dẫn dắt: Ngân hàng, Chứng khoán\n"
        "⚠️ Khuyến nghị: Quan sát – không FOMO"
    )

# =====================
# REGISTER HANDLERS
# =====================
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CommandHandler("market", market))

# =====================
# WEBHOOK ENDPOINT
# =====================
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return {"ok": True}

# =====================
# SET WEBHOOK ON START
# =====================
@app.on_event("startup")
async def on_startup():
    await tg_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
