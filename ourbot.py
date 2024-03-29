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
            return extract_email_details(email_body)
        else:
            return None


# Function to extract the email details
def extract_email_details(email_body):
    msg = email.message_from_bytes(email_body)
    sender_match = re.search(r'From: (.+?) <', msg.get("From"))
    sender = sender_match.group(1) if sender_match else "Unknown Sender"
    date = msg.get("Date")
    content = extract_main_message(msg)
    company_name_match = re.search(r'registration of (.+?) Internship', content, re.IGNORECASE)
    company_name = company_name_match.group(1) if company_name_match else "Unknown Company"
    deadline_match = re.search(r'Deadline : (.+?)\n', content)
    deadline = deadline_match.group(1) if deadline_match else "Unknown Deadline"
    return f"Sender: {sender}\nDate: {date}\nCompany Name: {company_name}\nDeadline: {deadline}"


# Function to extract the main message from the email content
def extract_main_message(msg):
    main_message = ''
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                main_message += part.get_payload(decode=True).decode('utf-8', 'ignore').strip() + '\n'
    else:
        main_message = msg.get_payload(decode=True).decode('utf-8', 'ignore').strip()
    return main_message


# Handler for /search command
@bot.message_handler(commands=['search'])
def search_command(message):
    mail = "prafull.sonawane21@vit.edu"  # Specify the email address to search for
    email_details = search_latest_email(mail)
    if email_details:
        bot.reply_to(message, email_details)
    else:
        bot.reply_to(message, f"No email found from {mail}.")


# Start the bot
bot.polling()
