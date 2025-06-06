import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from config import BOT_TOKEN, ADMIN_ID, SCRAPE_INTERVAL_HOURS
from admin_commands import add_channel, remove_channel, list_channels, load_channels
from job_scraper import scrape_jobs

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Manual /postjob command
async def post_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        data = update.message.text.split(" ", 1)[1]
        title, desc, link = [i.strip() for i in data.split("|")]
        msg = f"🚀 <b>{title}</b>\n\n{desc}\n\n🔗 {link}"
        channels = load_channels()

        for ch in channels:
            try:
                await context.bot.send_message(chat_id=ch, text=msg, parse_mode="HTML")
            except Exception as e:
                logging.error(f"Failed to send to {ch}: {e}")

        await update.message.reply_text("✅ Job posted.")
    except Exception as e:
        await update.message.reply_text("❗ Usage: /postjob Title | Description | Link")
        logging.error(e)

# Auto scraping job
async def auto_scrape_and_post(app: Application):
    jobs = scrape_jobs()
    channels = load_channels()
    for title, link in jobs:
        msg = f"📢 <b>{title}</b>\n🔗 {link}"
        for ch in channels:
            try:
                await app.bot.send_message(chat_id=ch, text=msg, parse_mode="HTML")
            except Exception as e:
                logging.error(f"Posting error to {ch}: {e}")

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("postjob", post_job))
    app.add_handler(CommandHandler("addchannel", add_channel))
    app.add_handler(CommandHandler("removechannel", remove_channel))
    app.add_handler(CommandHandler("listchannels", list_channels))

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: auto_scrape_and_post(app), 'interval', hours=SCRAPE_INTERVAL_HOURS)
    scheduler.start()

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
