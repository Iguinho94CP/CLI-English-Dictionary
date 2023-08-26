import os
from colorama import Fore, Style

class Helpers:
    def __init__(self):
        pass
    
    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def shorten_description(self, description, max_length=60):
        if len(description) > max_length:
            shortened = description[:max_length-3] + "..."
            return shortened
        return description
    
    def display_full_description(self, word):
        self.clear_console()
        print(f"\nFull description of {word.word}:\n")
        print(word.meaning)

        input("\nPress Enter to continue...")
    
    def get_valid_input(self, prompt, validation_func, err_msg, max_attempts=3):
        for _ in range(max_attempts):
            try:
                input_value = input(prompt)
                if validation_func(input_value):
                    return input_value
            except Exception as e:
                print(Fore.RED + f"{err_msg}".center(50, "-") + Style.RESET_ALL)
        print(Fore.RED + f"Exceeded max attempts ({max_attempts})".center(50, "-") + Style.RESET_ALL)
    
    def display_error(self, err_msg):
        print(Fore.RED + f"{err_msg}".center(50, "-") + Style.RESET_ALL)
        self.pause()
    
    def invalid_choice(self):
        print(Fore.RED + "Invalid choice".center(50, "-") + Style.RESET_ALL)
        self.pause()
    
    def pause(self):
        input("Press any key to continue...")
    
    def exit(self):
        self.clear_console()
        print(Fore.GREEN + "Goodbye!".center(50, "-") + Style.RESET_ALL)