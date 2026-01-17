import os
import logging
import requests
import xml.etree.ElementTree as ET
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://ten-app.onrender.com

if not BOT_TOKEN or not WEBHOOK_URL:
    raise RuntimeError("❌ Thiếu BOT_TOKEN hoặc WEBHOOK_URL")

# ================== LOG ==================
logging.basicConfig(level=logging.INFO)

# ================== FASTAPI ==================
app = FastAPI()

# ================== TELEGRAM ==================
tg_app = Application.builder().token(BOT_TOKEN).build()

# ================== DATA SOURCES ==================
def get_vnindex():
    url = "https://iboard.ssi.com.vn/dchart/api/index/VNINDEX"
    data = requests.get(url, timeout=10).json()
    return f"VNINDEX: {data['data'][-1]['close']}"

def get_news():
    rss_url = "https://cafef.vn/rss/cung-cap-thong-tin-chung-khoan.rss"
    xml = requests.get(rss_url, timeout=10).text
    root = ET.fromstring(xml)

    items = root.findall(".//item")[:3]
    news = "📰 TIN CHỨNG KHOÁN\n\n"

    for item in items:
        news += f"• {item.find('title').text}\n"

    return news

# ================== COMMANDS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 BOT CHỨNG KHOÁN VIỆT NAM\n\n"
        "/bangtin - Bảng tin thị trường\n"
        "/tintuc - Tin chứng khoán\n"
        "/auto - Bật auto 15 phút"
    )

async def bangtin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📊 BẢNG TIN THỊ TRƯỜNG\n\n{get_vnindex()}"
    )

async def tintuc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_news())

async def auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    context.job_queue.run_repeating(
        auto_job,
        interval=900,
        first=5,
        chat_id=chat_id,
        name=str(chat_id)
    )

    await update.message.reply_text("✅ Auto 15 phút đã bật")

# ================== AUTO JOB ==================
async def auto_job(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=f"⏰ AUTO UPDATE\n\n{get_vnindex()}"
    )

# ================== ROUTES ==================
@app.on_event("startup")
async def startup():
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(CommandHandler("bangtin", bangtin))
    tg_app.add_handler(CommandHandler("tintuc", tintuc))
    tg_app.add_handler(CommandHandler("auto", auto))

    await tg_app.initialize()
    await tg_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    await tg_app.start()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return {"ok": True}

@app.get("/")
def health():
    return "OK"
