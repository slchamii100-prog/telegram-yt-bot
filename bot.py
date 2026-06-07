import os
import re
import yt_dlp

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import os

BOT_TOKEN = os.getenv("7880694341:AAFIrEV2ql1mO_sfMhXTRv89J9VMMdm2lfg")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me a video link (YouTube, TikTok, Instagram, etc.)"
    )


def download_video(url):
    output_file = "video.%(ext)s"

    ydl_opts = {
        "outtmpl": output_file,
        "format": "mp4/best",
        "noplaylist": True,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return filename


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not re.match(r"https?://", text):
        return

    msg = await update.message.reply_text("Downloading...")

    try:
        file_path = download_video(text)

        with open(file_path, "rb") as video:
            await update.message.reply_video(video)

        os.remove(file_path)

        await msg.edit_text("Done.")

    except Exception as e:
        await msg.edit_text(f"Error: {e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link)
    )

    app.run_polling()


if __name__ == "__main__":
    main()