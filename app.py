import os
from flask import Flask, request
import telebot
from deep_translator import GoogleTranslator

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def receive_update():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

@bot.channel_post_handler(func=lambda message: True)
def translate_post(message):
    if message.text:
        translated = GoogleTranslator(source='auto', target='uz').translate(message.text)
        bot.send_message(CHANNEL_USERNAME, translated)

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run()
