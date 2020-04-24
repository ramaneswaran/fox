import logging
from requests import get
from bs4 import BeautifulSoup

class Scraper:
    '''
    This is the scraper class
    '''

    def __init__(self):
        '''
        Constructor class for Scraper
        '''
        logging.info("Loading Scraper")
        self.base_url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q='

    def scrape(self, topic):
        '''
        This function scrapes the research papers
        '''
        response = get(self.base_url+topic)
        
        if response.status_code == 200:
            logging.info("Response recieved")
        soup = BeautifulSoup(response.text,'html.parser')
            
        # Titles of the papers
        titles = [tag.find('a').text if tag.find('a') else 'Not found' for tag in soup.find_all('h3', class_='gs_rt')]
        
        # Link to the papers
        links = [tag.find('a').get('href') if tag.find('a') else 'Not found' for tag in soup.find_all('h3', class_='gs_rt')]

        # List of authors of the papers
        authors_list = [author_list.find_all('a') for author_list in soup.find_all('div', class_='gs_a')]
        authors = []
        for author_list in authors_list:
            authors.append(','.join([author.get_text() for author in author_list]))

        # Abstract of the papers
        abstracts = [abstract.get_text() for abstract in soup.find_all('div', class_='gs_rs')]
        result = []
        for i in range(len(titles)):
            result.append(
                {
                    'title':titles[i],
                    'authors':authors[i],
                    'abstract':abstracts[i],
                    'link':links[i]
                }
            )

        return result