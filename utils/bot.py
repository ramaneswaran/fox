import os
import time
import telebot
from fuzzywuzzy import fuzz

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

        self.brick = None

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

        @self.bot.message_handler(func = lambda message : True)
        def track_messages(message):
            '''
            This function tracks user messages
            '''

            if self.brick is not None:

                # That means this corresponds to a request
                if self.brick.command == 'paper':
                    # The request was for relevant papers
                    self.send_papers(message.text)
                
                elif self.brick.command == 'summary':
                    # Request was for summary
                    self.send_summary(message.text)
            
            else:
                if self.hacky_inference(message.text):
                    # The bot has been called
                    seld.send_greet()
                
        
        while True:
            try:
                self.bot.polling()
            except:
                time.sleep(15)
        
    def hacky_inference(self, text):
        '''
        This function checks if bot is called
        '''

        call_list = ['hey','hey athena','athena','help please','help']

        text = text.lower()

        for call in call_list:
            if fuzz.ratio(call, text) > 90:
                return True
        
        return False
    
    def menu_markup(self):
        '''
        This function generates a markup
        '''

        markup = types.InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(types.InlineKeyboardButton("Get Papers", callback_data="paper"),
                    types.InlineKeyboardButton("Get Summary", callback_data="summary"))
        
        return markup

    
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