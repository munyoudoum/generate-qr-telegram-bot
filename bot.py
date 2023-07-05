import logging
import os

from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

import qrcode


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# PORT = int(os.environ.get("PORT", 8443))
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Hi {user.mention_markdown_v2()}\! "
        "Send any text or link to generate a QR code image\!",
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Send any text or link to generate a QR code image!")


def create_qr(update: Update, context: CallbackContext, transparent=True) -> None:
    """Create QR from the user message."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(update.message.text)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    if transparent:
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)

    tmp_filename = "tmp_qrcode.png"
    img.save(tmp_filename)
    
    update.message.bot.send_photo(
        update.message.chat.id, photo=open(tmp_filename, "rb")
    )


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - create QR from the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, create_qr))

    # Start the Bot locally
    updater.start_polling()

    # Host the Bot in Heroku
    # updater.start_webhook(
    #     listen="0.0.0.0",
    #     port=int(PORT),
    #     url_path=TOKEN,
    #     webhook_url="https://your-app-name.herokuapp.com/" + TOKEN,
    # )

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
