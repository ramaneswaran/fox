import os
import logging
from dotenv import load_dotenv

# Loading utility modules
from utils.bot import TeleBot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    #TOKENS
    load_dotenv()

    bot_token = os.getenv('BOT_TOKEN')

    athena = TeleBot(bot_token)
    logging.info("Activating Athena")
    athena.activate()
    
