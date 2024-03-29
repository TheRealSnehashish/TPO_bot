import re
import email
from imapclient import IMAPClient
import telebot
from dotenv import load_dotenv
import os

load_dotenv()
# Telegram Bot token
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

# Email account credentials
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_USERNAME = os.environ["EMAIL_USERNAME"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

# Initialize the Telegram Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Function to search for the latest email associated with the provided email address
def search_latest_email(email_address):
    with IMAPClient(EMAIL_HOST) as server:
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.select_folder('INBOX')
        messages = server.search(['FROM', email_address])
        if messages:
            # Fetch the latest email
            latest_email_id = messages[-1]
            email_data = server.fetch(latest_email_id, ['BODY[]'])
            email_body = email_data[latest_email_id][b'BODY[]']
            return extract_main_message(email_body)
        else:
            return None


# Function to extract the main message from the email content
def extract_main_message(email_body):
    msg = email.message_from_bytes(email_body)
    main_message = ''
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                main_message += part.get_payload(decode=True).decode('utf-8', 'ignore').strip() + '\n'
    else:
        main_message = msg.get_payload(decode=True).decode('utf-8', 'ignore').strip()
    return main_message


# Handler for /search command with email address
@bot.message_handler(commands=['search'])
def search_command_with_email(message):
    # Extract the email address from the message text
    # email_address = message.text.split(maxsplit=1)[1]
    mail = "prafull.sonawane21@vit.edu"
    # Search for the latest email associated with the given email address
    email_content = search_latest_email(mail)

    if email_content:
        bot.reply_to(message, f"Latest email for {mail}:\n{email_content}")
    else:
        bot.reply_to(message, f"No email found for {mail}.")


# Start the bot
bot.polling()
