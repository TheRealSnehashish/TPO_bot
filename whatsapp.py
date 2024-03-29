# Import necessary libraries
import telebot
from imapclient import IMAPClient

# Telegram Bot token
TELEGRAM_TOKEN = '7026916796:AAGXGQPaUbAWXjnP3LlVtSZbDuys2BQ_pSM'

# Email account credentials
EMAIL_HOST = 'imap.gmail.com'
EMAIL_USERNAME = 'snehashishmulgir221@gmail.com'
EMAIL_PASSWORD = 'cmxs wftp rgkf twne'

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
            email_body = email_data[latest_email_id][b'BODY[]'].decode('utf-8')
            return email_body
        else:
            return None

# Handler for /search command with email address
@bot.message_handler(commands=['search'])
def search_command_with_email(message):
    # Extract the email address from the message text
    # email_address = message.text.split(maxsplit=1)[1]
    mail = "prafull.sonawane21@vit.edu"
    # Search for the latest email associated with the given email address
    email_content = search_latest_email(mail)

    if email_content:
        # Split the email content into smaller chunks of 4096 characters (Telegram message length limit)
        chunks = [email_content[i:i + 4096] for i in range(0, len(email_content), 4096)]
        for chunk in chunks:
            bot.reply_to(message, f"Latest email for {mail}:\n{chunk}")
    else:
        bot.reply_to(message, f"No email found for {mail}.")

# Start the bot
bot.polling()
