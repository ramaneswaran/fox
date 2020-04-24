from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import math
import logging

class TextSummarizer:
    '''
    This is TextSummarizer class
    '''

    def __init__(self):
        '''
        Constructor class of TextSummarizer
        '''
        logging.info("Loading summarizer")
        # The language being processed
        language = 'english'

        # Loading the summarizer
        stemmer = Stemmer(language)

        self.summarizer =  Summarizer(stemmer)
        self.summarizer.stop_words = get_stop_words(language)

    def summary(self, content):
        '''
        This function summarizes text
        '''
        try:
            parser = PlaintextParser.from_string(content, Tokenizer('english'))
            logging.info("Parsed text")
            sent_count = 0
            for sentence in content.split('.'):
                sent_count+=1
            
            
            summary = self.summarizer(parser.document, math.ceil(sent_count*0.3))
        except Exception as error:
            logging.info(error)
        finally:
            return summary if summary else None



