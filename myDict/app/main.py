import requests
from app.models.models import *
from .scrapers.thesaurus import ThesaurusScraper
from .scrapers.word_of_the_day import WordOfTheDayExtractor
from colorama import Fore, Style, init
from .utils.helpers import Helpers
from datetime import datetime

class MyDict:
    def __init__(self, database):
        # Initialize attributes
        self.database = database
        self.wordOfTheDay = None
        self.thesaurus = None
        self.display_helpers = Helpers()

        # Initialize scraper instances
        self.thesaurus = ThesaurusScraper()
        self.wordOfTheDay = WordOfTheDayExtractor()

        # Get a session from the database
        self.session = self.database.get_session()
    
    def menu(self):
        while True:
            self.display_helpers.clear_console()
            print(Fore.CYAN + "MyDict - Menu" + Style.RESET_ALL)
            print(Fore.GREEN + "1. Add a word" + Style.RESET_ALL)
            print(Fore.GREEN + "2. Word of the day" + Style.RESET_ALL)
            print(Fore.GREEN + "3. Show words" + Style.RESET_ALL)
            print(Fore.GREEN + "4. Exit" + Style.RESET_ALL)
            
            choice = input(Fore.GREEN + "Enter your choice: " + Style.RESET_ALL)
            
            if choice == "1":
                self.addWord()
            elif choice == "2":
                self.display_word_of_the_day()
            elif choice == "3":
                self.show_words()
            elif choice == "4":
                self.exit()
                break
            else:
                self.invalid_choice()
    
    def fetch_meanings_from_api(self, word):
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            meanings = []
            for entry in data:
                for meaning in entry.get("meanings", []):
                    definitions = meaning.get("definitions", [])
                    if definitions:
                        meanings.append(definitions[0]["definition"])
            return meanings
        else:
            return None
    
    def addWord(self):
        
        try:
            self.display_helpers.clear_console()
            word = self.display_helpers.get_valid_input(Fore.CYAN + "Enter a word: ",
                    lambda x: x.isalpha(),
                    Fore.WHITE + "Invalid input. Please enter a valid word."
                ).capitalize()
            
            meanings = self.fetch_meanings_from_api(word)
            if meanings:
                meaning = ", ".join(meanings)
            else:
                meaning = self.display_helpers.get_valid_input(
                    Fore.CYAN + "Enter a meaning: ",
                    lambda x: x.isalpha(),
                    Fore.WHITE + "Invalid input. Please enter a valid meaning."
                )
            
            word_entry = self.session.query(Word).filter_by(word=word).first()
            if word_entry:
                print(Fore.GREEN + f"Word already exists" + Style.RESET_ALL)
                return
            
            new_word = Word(
                word=word,
                meaning=meaning,
            )
            self.session.add(new_word)
            self.session.commit()
            
            self.thesaurus.set_word(word)
            synonyms, antonyms = self.thesaurus.run()
            
            existing_word = self.session.query(Thesaurus).filter_by(word_id=new_word.id).first()
            if existing_word:
                existing_word.synonym = list(set(existing_word.synonym + synonyms))
                existing_word.antonym = list(set(existing_word.antonym + antonyms))
            else:
                new_thesaurus = Thesaurus(
                    synonym=synonyms,
                    antonym=antonyms,
                    word_id=new_word.id
                )
                self.session.add(new_thesaurus)
            self.session.commit()
            
            print(Fore.GREEN + f"Word added successfully" + Style.RESET_ALL)
            self.display_helpers.pause()
        
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
    
    def display_word_of_the_day(self):
        self.display_helpers.clear_console()
        time, word = self.wordOfTheDay.extract_word_of_the_day()
        print(f"\nWord of the day: {word}")
        print(f"Time: {time}")
        
        meanings = self.fetch_meanings_from_api(word)  # Pass the word to fetch_meanings_from_api()
        if meanings:
            meaning = ", ".join(meanings)
        else:
            meaning = self.display_helpers.get_valid_input(
                Fore.CYAN + "Enter a meaning: ",
                lambda x: x.isalpha(),
                Fore.WHITE + "Invalid input. Please enter a valid meaning."
            )
            
        existing_word = self.session.query(WordOfTheDay).filter_by(word=word).first()
        if existing_word:
            self.display_helpers.pause()
            return existing_word
        else:
            word_of_the_day = WordOfTheDay(
                word=word,
                meaning=meaning,
                date=datetime.strptime(time, "%B %d, %Y")
            )
            self.session.add(word_of_the_day)
            self.session.commit()
            
            print(Fore.GREEN + "Word of the day added successfully!")
            self.display_helpers.pause()
    
    def show_words(self):
        page_size = 10  # Number of words to display per page
        start_index = 0  # Starting index for the current page

        number_colors = [Fore.WHITE, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.YELLOW]
        color_index = 0

        while True:
            self.display_helpers.clear_console()
            print(Fore.YELLOW + "Displaying words\n")
            try:
                words = self.session.query(Word).all()
                words_of_the_day = self.session.query(WordOfTheDay).all()
                total_words = len(words)
                total_words_of_the_day = len(words_of_the_day)

                for index in range(start_index, min(start_index + page_size, total_words)):
                    word = words[index]
                    number_color = number_colors[color_index % len(number_colors)]
                    description_color = Fore.RESET  # Reset color for description lines

                    print(number_color + f"{index - start_index + 1}. {word.word}")
                    print(description_color + f"   {self.display_helpers.shorten_description(word.meaning)}")
                    print()

                word_of_the_day = self.session.query(WordOfTheDay).order_by(WordOfTheDay.date.desc()).first()
                if word_of_the_day:
                    print(Fore.CYAN + "Word of the day:")
                    print(f"   {word_of_the_day.word}\n")
                    print()
                else:
                    print(Fore.WHITE + "No word of the day found.")

                print("0. Go back")
                print("P. Previous page")
                print("N. Next page")
                choice = input(Style.BRIGHT + "Enter your choice: ")

                if choice == "0":
                    break
                elif choice.lower() == "p" and start_index - page_size >= 0:
                    start_index -= page_size
                elif choice.lower() == "n" and start_index + page_size < max(total_words, total_words_of_the_day):
                    start_index += page_size
                # Add other cases for handling navigation
                elif choice.isdigit() and 1 <= int(choice) <= min(page_size, total_words - start_index + 1):
                    selected_word = words[start_index + int(choice) - 1]
                    self.display_helpers.display_full_description(selected_word)
                    self.submenu(selected_word)

                color_index += 1

            except Exception as e:
                self.display_helpers.display_error(e)

    
    def submenu(self, word):
        while True:
            self.display_helpers.clear_console()
            print(Fore.CYAN + "MyDict - Submenu" + Style.RESET_ALL)
            print(Fore.GREEN + "1. Update word" + Style.RESET_ALL)
            print(Fore.GREEN + "2. Delete word" + Style.RESET_ALL)
            print(Fore.GREEN + "3. Go back" + Style.RESET_ALL)
            choice = input(Fore.GREEN + "Enter your choice: " + Style.RESET_ALL)
            
            if choice == "1":
                self.update_word(word)
            elif choice == "2":
                self.delete_word(word)
                break
            elif choice == "3":
                break
            else:
                self.display_helpers.invalid_choice()
