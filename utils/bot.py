import os
import time
import telebot

# Import utility classes
from utils.scraper import Scraper
from utils.rake import Raker
from utils.summarizer import TextSummarizer

class TeleBot:
    '''
    This is the class which initializes a telegram bot
    '''

    def __init__(self, bot_token):
        '''
        The constructor for TeleBot class
        '''

        self.bot = telebot.TeleBot(token=bot_token, threaded=False)

        self.scraper = Scraper()

        self.raker = Raker()

        self.text_summarizer = TextSummarizer()

    def activate(self):
        '''
        This function activates the bot and listens to messages
        '''

        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            '''
            This function is used to test if bot is active
            '''
            self.bot.reply_to(message, 'Bot is active and listening')

        while True:
            try:
                self.bot.polling()
            except:
                time.sleep(15)
    
    def get_brick(self, command):
        '''
        Returns a brick for a command request
        '''

        brick = {
            'command': command,
            'complete': False
        }

        return brick
        
    def get_papers(self, abstract):
        '''
        This paper returns relevant research papers
        '''

        # Get a list of keywords
        keywords = self.raker.get_keywords(abstract, 4)

        # Form a topic
        topic = keywords.join(' ')

        paper_metadata = self.scraper.scrape(topic)

        return paper_metadata

    def get_summary(self, content):
        '''
        This paper returns summary
        '''

        summary = self.text_summarizer.summary(content)

        return summary