import os
import time
import logging
import telebot
from telebot import types
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

        self.menu = self.menu_markup()

    def activate(self):
        '''
        This function activates the bot and listens to messages
        '''

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            '''
            This function is the callback query handler
            '''

            if call.data == 'paper':
                # Track the command
                self.brick = self.get_brick('paper')

                # Intimate the user
                self.bot.send_message(call.message.chat.id, "Please enter the paper abtract below")

            elif call.data == 'summary':
                # Track the command
                self.brick = self.get_brick('summary')

                # Intimate the user
                self.bot.send_message(call.message.chat.id, "Please enter the text to be summarized")


        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            '''
            This function is used to test if bot is active
            '''
            self.bot.reply_to(message, 'Athena is active and listening')

        @self.bot.message_handler(func = lambda message : True)
        def track_messages(message):
            '''
            This function tracks user messages
            '''
            
            if self.brick is not None:

                # That means this corresponds to a request
                if self.brick['command'] == 'paper':
                    # The request was for relevant papers
                    logging.info("Here for papers")
                    self.send_papers(message.text, message.chat.id)
                
                elif self.brick['command'] == 'summary':
                    # Request was for summary
                    self.send_summary(message.text, message.chat.id)
            
            else:
                if self.hacky_inference(message.text):
                    # The bot has been called
                    self.send_greet(message.chat.id)
                
        
        while True:
            try:
                self.bot.polling()
            except:
                time.sleep(15)
        
    def send_greet(self, chat_id):
        '''
        This function greets and presents options
        '''
        
        text = "*Hey! Its Athena* 🕵️‍♀️ \nPlease click the service you wish to request "

        self.bot.send_message(chat_id, text, reply_markup=self.menu,
                             parse_mode="Markdown")
    
    
    def send_papers(self, abstract, chat_id):
        '''
        This papers send the papers to user
        '''

        paper_metadata = self.get_papers(abstract)

        for item in paper_metadata:
            text = "*"+item['title']+"*\n"
            text += "[Click here to visit paper]("+item['link']+")"
            self.bot.send_message(chat_id, text, parse_mode="Markdown")
        
        # Clear the brick
        self.brick = None

    def send_summary(self, content, chat_id):
        '''
        This paper sends the summary to the user
        '''

        summary = self.get_summary(content)

        # Intimate the user about the incoming summary
        self.bot.send_message(chat_id, "The text has been summarized below: ")

        for sentence in summary:
            self.bot.send_message(chat_id, sentence)
        
        # Clear the brick
        self.brick = None
        
    def hacky_inference(self, text):
        '''
        This function checks if bot is called
        '''

        call_list = ['hey','hey athena','athena','help please','help']

        text = text.lower()
        

        for call in call_list:
            ratio = fuzz.ratio(call, text)
            
            if ratio > 90:
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
        logging.info("Keywords generated")

        # Form a topic
        topic = ' '.join(keywords)
        
        paper_metadata = self.scraper.scrape(topic)
        logging.info("Papers scraped")

        return paper_metadata

    def get_summary(self, content):
        '''
        This paper returns summary
        '''

        summary = self.text_summarizer.summary(content)

        return summary

    