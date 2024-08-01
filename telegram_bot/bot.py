import logging
import sys

import requests
from decouple import config
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

HOST_BASE_URL = config("HOST_BASE_URL", None)
TELEGRAM_API_KEY = config("TELEGRAM_TOKEN", None)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.API_KEY = TELEGRAM_API_KEY
        self.CHOOSING_OPTION = 0
        self.reply_keyboard = [["GET List of Books"]]

        self.validate_api_key_not_empty()

    def validate_api_key_not_empty(self) -> None:
        if not self.API_KEY:
            logger.error(
                "API key not found. "
                "Please set the valid TELEGRAM_API_KEY environment variable."
                "Closing the application..."
            )
            sys.exit(1)

    async def start(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        await update.message.reply_text(
            "Hi! I'm the *Books Telegram bot*.\n"
            "Press 'GET List of Books' to get the data from the API.",
            parse_mode="markdown",
            disable_web_page_preview=True,
            reply_markup=ReplyKeyboardMarkup(self.reply_keyboard),
        )
        return self.CHOOSING_OPTION

    async def handle_user_choice(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        user_choice = update.message.text

        if user_choice == "GET List of Books":
            data = self.fetch_books_data()
            await update.message.reply_text(data, parse_mode="markdown")
            return self.CHOOSING_OPTION

        if user_choice in ["exit", "cancel"]:
            await update.message.reply_text(
                "Bye!", reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END
        else:
            await update.message.reply_text("Invalid option selected.")
            return self.CHOOSING_OPTION

    @staticmethod
    def fetch_books_data() -> str:
        try:
            response = requests.get(f"{HOST_BASE_URL}api/books/")
            response.raise_for_status()
            answer_string = ""
            print(response.json())
            for result in response.json():
                text = (
                    f"*title:* {result['title']}\n"
                    f"*author:* {result['author']}\n"
                    f"*price:* {result['price']} USD\n"
                )
                answer_string += f"{text}\n"
            return answer_string
        except requests.RequestException as e:
            logger.error(f"Error fetching data: {e}")
            return "Failed to fetch data."

    async def exit(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        await update.message.reply_text("Conversation closed.")
        return ConversationHandler.END

    async def error_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        logger.error("Exception occurred:", exc_info=context.error)

    def main(self) -> None:
        logger.info("Running telegram bot...")
        application = Application.builder().token(self.API_KEY).build()

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                self.CHOOSING_OPTION: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        self.handle_user_choice,
                    )
                ],
            },
            fallbacks=[
                CommandHandler("exit", self.exit),
                CommandHandler("quit", self.exit),
            ],
        )
        application.add_handler(conv_handler)
        application.run_polling()


if __name__ == "__main__":
    TelegramBot().main()
