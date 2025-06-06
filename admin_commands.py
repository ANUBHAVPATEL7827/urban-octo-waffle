import json
from config import ADMIN_ID
from telegram import Update
from telegram.ext import ContextTypes

CHANNEL_FILE = "channels.json"

def load_channels():
    with open(CHANNEL_FILE, "r") as f:
        return json.load(f)["channels"]

def save_channels(channels):
    with open(CHANNEL_FILE, "w") as f:
        json.dump({"channels": channels}, f)

async def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.effective_user.id):
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /addchannel @channelusername")
        return

    channel = context.args[0]
    channels = load_channels()

    if channel not in channels:
        channels.append(channel)
        save_channels(channels)
        await update.message.reply_text(f"✅ Added {channel}")
    else:
        await update.message.reply_text("Channel already exists.")

async def remove_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.effective_user.id):
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /removechannel @channelusername")
        return

    channel = context.args[0]
    channels = load_channels()

    if channel in channels:
        channels.remove(channel)
        save_channels(channels)
        await update.message.reply_text(f"❌ Removed {channel}")
    else:
        await update.message.reply_text("Channel not found.")

async def list_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.effective_user.id):
        return

    channels = load_channels()
    if channels:
        await update.message.reply_text("\n".join(channels))
    else:
        await update.message.reply_text("No channels configured.")
