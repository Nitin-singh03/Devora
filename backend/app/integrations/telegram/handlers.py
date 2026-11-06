from telegram import Update
from telegram.ext import ContextTypes

from app.core.config import settings
from app.db.database import SessionLocal

from app.modules.dsa.progress.service import (
    get_overall_progress,
    get_weak_topics
)

from app.modules.dsa.planner.service import (
    create_study_plan
)


async def authorize(update: Update):
    telegram_user = update.effective_user

    if not telegram_user:
        return False

    if telegram_user.id != settings.TELEGRAM_ALLOWED_USER_ID:
        await update.effective_message.reply_text(
            "You are not authorized to use Devora."
        )
        return False

    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await authorize(update):
        return

    await update.message.reply_text(
        "Welcome to Devora!\n\n"
        "Your personal DSA assistant.\n\n"
        "Available commands:\n"
        "/progress - View your progress\n"
        "/weak - View weak topics\n"
        "/today - View today's study plan\n"
        "/help - Show commands"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await authorize(update):
        return

    await update.message.reply_text(
        "/progress - Your overall progress\n"
        "/weak - Your weak topics\n"
        "/today - Your study plan"
    )


async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await authorize(update):
        return

    db = SessionLocal()

    try:
        result = get_overall_progress(
            settings.DEVORA_USER_ID,
            db
        )

        message = (
            "Your DSA Progress\n\n"
            f"Attempted: {result['attempted']}\n"
            f"Solved: {result['solved']}\n"
            f"Submissions: {result['submissions']}\n"
            f"Success Rate: {result['success_rate']}%"
        )

        await update.message.reply_text(message)

    finally:
        db.close()


async def weak(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await authorize(update):
        return

    db = SessionLocal()

    try:
        topics = get_weak_topics(
            settings.DEVORA_USER_ID,
            db
        )

        if not topics:
            await update.message.reply_text(
                "No weak topics identified yet."
            )
            return

        message = "Your Weak Topics\n\n"

        for topic in topics:
            message += (
                f"{topic['topic']}: "
                f"{topic['success_rate']}% success rate\n"
            )

        await update.message.reply_text(message)

    finally:
        db.close()


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await authorize(update):
        return

    db = SessionLocal()

    try:
        result = create_study_plan(
            settings.DEVORA_USER_ID,
            db
        )

        items = result["items"]

        if not items:
            await update.message.reply_text(
                "Your study plan is empty today."
            )
            return

        message = "Your Study Plan\n\n"

        for index, item in enumerate(items, start=1):
            message += (
                f"{index}. {item['title']} "
                f"({item['type']})\n"
            )

        await update.message.reply_text(message)

    finally:
        db.close()