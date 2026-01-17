import os
import requests
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")       # token bot telegram
WEBHOOK_URL = os.getenv("WEBHOOK_URL")   # https://xxx.onrender.com
CHAT_ID = os.getenv("CHAT_ID")           # chat id / channel id

if not BOT_TOKEN or not WEBHOOK_URL:
    raise RuntimeError("❌ Missing BOT_TOKEN or WEBHOOK_URL")

# ================== APP ==================
app = FastAPI()
tg_app = Application.builder().token(BOT_TOKEN).build()

# ================== COMMANDS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Bot Chứng Khoán Việt Nam đã sẵn sàng!\n"
        "/bangtin - Bảng tin thị trường\n"
        "/vnindex - VNINDEX hiện tại\n"
        "/help - Hướng dẫn"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Danh sách lệnh:\n"
        "/bangtin\n"
        "/vnindex"
    )

async def vnindex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://api.ssi.com.vn/api/market/vnindex")
        data = r.json()
        index = data.get("data", {}).get("index", "N/A")
        change = data.get("data", {}).get("change", "N/A")
        await update.message.reply_text(
            f"📈 VNINDEX\n"
            f"Giá: {index}\n"
            f"Thay đổi: {change}"
        )
    except:
        await update.message.reply_text("⚠️ Không lấy được dữ liệu VNINDEX")

async def bangtin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📰 BẢNG TIN THỊ TRƯỜNG\n"
        "- VNINDEX dao động\n"
        "- Dòng tiền phân hóa\n"
        "- Ngân hàng & thép đáng chú ý"
    )

# ================== HANDLERS ==================
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CommandHandler("help", help_cmd))
tg_app.add_handler(CommandHandler("vnindex", vnindex))
tg_app.add_handler(CommandHandler("bangtin", bangtin))

# ================== WEBHOOK ==================
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    await tg_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    print("🚀 Bot started successfully")

@app.get("/")
async def root():
    return {"status": "running"}
