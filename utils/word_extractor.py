from multi_rake import Rake 

class WordExtractor:
    '''
    This is the WordExtractor class
    '''

    def __init__(self):
        '''
        This is is the constructor function for WordExtractor
        '''

        self.rake = Rake()

    def get_keywords(self, text, number):
        '''
        This function returns keywords
        '''

        kw_data = self.rake.apply(text)

        kw_list = [kw_tuple[0] for kw_tuple in kw_data[:number]]

        return kw_list