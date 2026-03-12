# bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import asyncio

BOT_TOKEN = "8789370521:AAEIwwdt9jtmIzMbSylfLcM3Rl5B-OIlLjE"

# ----- Ollama helper -----
def ask_ai(question: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": question,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        return response.json()["response"]

    except Exception as e:
        print("Ollama error:", e)
        return "Sorry, the AI could not respond."

# ----- Handlers -----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a question.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"Received: {user_text}")

    answer = ask_ai(user_text)

    await update.message.reply_text(answer)

# ----- Main -----
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot is running...")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app.run_polling())

if __name__ == "__main__":
    main()