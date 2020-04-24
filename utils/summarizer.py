from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import math

class TextSummarizer:
    '''
    This is TextSummarizer class
    '''

    def __init__(self):
        '''
        Constructor class of TextSummarizer
        '''

        # The language being processed
        language = 'english'

        # Loading the summarizer
        stemmer = Stemmer(self.language)

        self.summarizer Summarizer(stemmer)
        self.summarizer.stop_words = get_stop_words(language)

    def summary(self, content):
        '''
        This function summarizes text
        '''
        parser = PlaintextParser.from_string(content, Tokenizer(LANGUAGE))

        sent_count = 0
        for sentence in content.split('.'):
            sent_count+=1
        
        
        summary = summarizer(parser.document, math.ceil(sent_count*0.3))

        return summary



