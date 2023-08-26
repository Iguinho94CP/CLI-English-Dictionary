import requests
from bs4 import BeautifulSoup

class WordOfTheDayExtractor:
    def __init__(self):
        self.last_extracted_date = None
        self.last_extracted_word = None

    def extract_word_of_the_day(self):
        url = 'https://www.dictionary.com/'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        extracted_time = soup.find('time', {'class': 'TQAdWb5A36CZSEUVopqN'}).text
        word_of_the_day = soup.find('a', {'class': 'hJCqtPGYwMx5z04f6y2o'}).text

        return extracted_time, word_of_the_day
    
    def run(self):
        extracted_time, word_of_the_day = self.extract_word_of_the_day()
        self.last_extracted_date = extracted_time
        self.last_extracted_word = word_of_the_day
        return word_of_the_day

if __name__ == '__main__':
    word_of_the_day_extractor = WordOfTheDayExtractor()
    word_of_the_day = word_of_the_day_extractor.run()
    print(word_of_the_day)
