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

# =========================
# ENV
# =========================
BOT_TOKEN = os.getenv("8293088764:AAEtieskYMNNHcFLja2N9o0Y5kT7aJe5t8g")        # 🔴 token BotFather
CHANNEL_ID = os.getenv("-1003648760665")      # 🔴 -100xxxxxxxxxx
WEBHOOK_URL = os.getenv("https://telegram-bot-miyz.onrender.com/webhook")    # 🔴 https://ten-app.onrender.com/webhook
PORT = int(os.getenv("PORT", 10000))

# =========================
# LOG
# =========================
logging.basicConfig(level=logging.INFO)

# =========================
# BOT HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot chứng khoán đã hoạt động!\n\n"
        "/bangtin – Bảng tin thị trường\n"
        "/nhan_dinh – Nhận định\n"
        "/khuyen_nghi – Khuyến nghị\n"
        "/post <nội dung> – Đăng channel"
    )

async def bang_tin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 BẢNG TIN THỊ TRƯỜNG\n"
        "• VNINDEX: cập nhật\n"
        "• Thanh khoản: cập nhật\n"
