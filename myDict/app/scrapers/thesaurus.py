import requests
from bs4 import BeautifulSoup
import random

class ThesaurusScraper:
    BASE_URL_TEMPLATE = "https://www.thesaurus.com/browse/{}"

    def __init__(self):
        self.word = None
        self.response = None
        self.soup = None
        self.BASE_URL = None

    def set_word(self, word):
        self.word = word
        self.BASE_URL = self.BASE_URL_TEMPLATE.format(word)

    def set_scraper(self):
        self.response = requests.get(self.BASE_URL)
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def _get_words_from_section(self, section_class):
        class_section = self.soup.find('section', {'class': section_class})
        if class_section:
            words = class_section.find_all('a')
            words_list = [word.text for word in words]
            return words_list
        return None

    def get_unique_words(self, words_list):
        return list(set(words_list))

    def get_first_word(self, words_list):
        return words_list[0] if words_list else None

    def get_synonym_and_antonym(self):
        synonym_section_class = 'q7ELwPUtygkuxUXXOE9t ULFYcLlui2SL1DTZuWLn'
        antonym_section_class = 'q7ELwPUtygkuxUXXOE9t sjTvA1Sebv19EFVyZvyp'

        synonym_words_list = self._get_words_from_section(synonym_section_class) or []
        antonym_words_list = self._get_words_from_section(antonym_section_class) or []

        # Shuffle the synonym and antonym lists
        random.shuffle(synonym_words_list)
        random.shuffle(antonym_words_list)

        synonym = self.get_first_word(self.get_unique_words(synonym_words_list))
        antonym = self.get_first_word(self.get_unique_words(antonym_words_list))

        return synonym, antonym

    def run(self):
        self.set_scraper()
        return self.get_synonym_and_antonym()