import os
import re
import shutil
from interacted import interacted
from scrape import scrape
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters


async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    reel_pattern = r'(https?://)?(www\.)?instagram\.com/reel/[A-Za-z0-9_-]+/?(\?utm_source=[^&\s]+(&[^\s]*)?)?'

    if not re.match(reel_pattern, url):
        await update.message.reply_text(
            "❌ Invalid link")
        return

    await update.message.reply_text(
        "✅ Valid link")
    await update.message.reply_text(
        "⬇️ Downloading...")

    try:
        download_folder = await scrape(url)
        downloaded_file = f'{download_folder}/{os.listdir(download_folder)[0]}'
        with open(downloaded_file, 'rb') as video_file:
            await update.message.reply_video(video_file)
    except Exception as e:
        await update.message.reply_text("❌ An error occurred, please try again")
        return
    finally:
        shutil.rmtree(download_folder)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    interacted(user)

    await update.message.reply_text(
        "Hello! Send me a Instagram Reels link to download MP4 video ✨")


def main():
    app = ApplicationBuilder().token(os.getenv('BOT_TOKEN')
                                     ).read_timeout(60).write_timeout(60).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, download_reel))

    app.run_polling()


if __name__ == "__main__":
    main()
