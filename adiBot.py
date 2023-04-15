from telegram import *
from telegram.ext import *
import logging
import random

from werkzeug.wrappers import response
from copilot import Copilot


TOKEN = ''
API_KEY = ''

# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

logger.info("BOT STARTED")

async def start_command(update, context):
    await update.message.reply_text("fuckk off!!")

async def option_command(update, context):
    keyboard = [
        [InlineKeyboardButton("Score", callback_data="score")],
        [InlineKeyboardButton("Help", callback_data="help")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)
    # await update.message.reply_text("Type something random to get started")

async def help_command(update, context):
    await update.message.reply_text("SADDSA")

async def image_command(update, context):
    """Sends an image"""

    text = str(update.message.text).lower()
    text = text[6:]
    response = _generate_copilot_image(text)

    media_1 = InputMediaDocument(media=response['url'])
    await context.bot.send_media_group(update.effective_chat.id, [media_1])
    # await context.bot.send_message(update.effective_chat.id, text)

def _generate_copilot_image(prompt: str):
    """Gets an image url"""

    copilot = Copilot()
    c = copilot.get_image(prompt)

    return c

def _generate_copilot_answer(prompt: str):
    """Gets answer from copilot"""
    
    copilot = Copilot()
    c = copilot.gpt_3(prompt)

    return c

async def chat_command(update, context):
    text = str(update.message.text).lower()
    response = _generate_copilot_answer(text)

    await context.bot.send_message(update.effective_chat.id, response)

async def toss_command(update, context):
    response = random.choice(['heads', 'tails'])

    await context.bot.send_message(update.effective_chat.id, response)

async def handle_message(update, context):
    text = str(update.message.text).lower()
    # response = _generate_copilot(text)

    await update.message.reply_text("Under Construction :)")

async def crickbuzz(update, context):
    import http.client
    conn = http.client.HTTPSConnection("cricbuzz-cricket.p.rapidapi.com")
    headers = {
            'X-RapidAPI-Key': API_KEY,
            'X-RapidAPI-Host': "cricbuzz-cricket.p.rapidapi.com"
            }
    conn.request("GET", "/series/v1/4061", headers=headers)
    res = conn.getresponse()
    data = res.read()
    import json
    dict = json.loads(data)
    dict = dict['matchDetails']
    dict = dict[len(dict)-1]
    dict = dict['matchDetailsMap']
    dict = dict['match']
    dict = dict[0]
    matchInfo = dict['matchInfo']
    await context.bot.send_message(update.effective_chat.id, matchInfo['status'])

async def score(update, context):
  import http.client

  conn = http.client.HTTPSConnection("cricbuzz-cricket.p.rapidapi.com")

  headers = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': "cricbuzz-cricket.p.rapidapi.com"
  }

  conn.request("GET", "/matches/v1/live", headers=headers)

  res = conn.getresponse()
  data = res.read()
  try:
      import json
      dict = json.loads(data)
      dict = dict['typeMatches']
      dict = dict[0]
      dict = dict['seriesMatches']
      dict = dict[0]
      dict = dict['seriesAdWrapper']
      dict = dict['matches']
      dict = dict[0]
  except:
        await context.bot.send_message(update.effective_chat.id, f"No match running :(")
        return

  matchInfo = dict['matchInfo']['status']
  team1 = dict['matchInfo']['team1']['teamSName']
  team2 = dict['matchInfo']['team2']['teamSName']
  try:
    team1Score = dict['matchScore']['team1Score']['inngs1']['runs']
    over1 = dict['matchScore']['team1Score']['inngs1']['overs']
  except:
    team1Score = ''
    over1 = ''
  try:
    team2Score = dict['matchScore']['team2Score']['inngs1']['runs']
    over2 = dict['matchScore']['team2Score']['inngs1']['overs']
  except:
    team2Score = ''
    over2 = ''
  await context.bot.send_message(
    update.effective_chat.id,
    f'{matchInfo}\n{team1}: {team1Score} of {over1}\n{team2}: {team2Score} of {over2}'
  )


async def poll(update, context):
    """Sends a predefined poll"""
    questions = ["Good", "Really good", "Fantastic", "Great"]
    message = await context.bot.send_poll(
        update.effective_chat.id,
        "How are you?",
        questions,
        is_anonymous=False,
        allows_multiple_answers=True,
    )
    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {
        message.poll.id: {
            "questions": questions,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.delete_message()

    # await query.edit_message_text(text=f"Selected option: {query.data}")

    if query.data == "help":
        await context.bot.send_message(update.effective_chat.id, "What the fuck? U need help bitch?")
    elif query.data == "score":
        await score(update = update, context = context)
    elif query.data == "crickbuzz":
        await crickbuzz(update = update, context = context)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("chat", chat_command))
    application.add_handler(CommandHandler("toss", toss_command))
    application.add_handler(CommandHandler("image", image_command))
    application.add_handler(CommandHandler("options", option_command))
    application.add_handler(CommandHandler("poll", poll))

    application.add_handler(CallbackQueryHandler(button))

    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    application.run_polling()

main()

# bot_token = '6048253507:AAFDrWOJV7DqlA5Dyrw3IUH8aYj6f9yG6ME'
# chat_id = '1212699113'
# message = 'Hello, world!'
# send_message(bot_token, chat_id, message)
