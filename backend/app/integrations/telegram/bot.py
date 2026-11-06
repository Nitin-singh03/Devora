from telegram.ext import (
    Application,
    CommandHandler
)

from app.core.config import settings

from app.integrations.telegram.handlers import (
    start,
    help_command,
    progress,
    weak,
    today
)


def main():

    application = (
        Application.builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CommandHandler("progress", progress)
    )

    application.add_handler(
        CommandHandler("weak", weak)
    )

    application.add_handler(
        CommandHandler("today", today)
    )

    print("Devora Telegram bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()