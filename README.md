# CLI Dictionary
## Main menu 
![Main menu](https://github.com/Iguinho94CP/CLI-English-Dictionary/blob/main/menu.png)
## Enter word option
![Main menu](https://github.com/Iguinho94CP/CLI-English-Dictionary/blob/main/enter_word.png)
## Word of the day
![Main menu](https://github.com/Iguinho94CP/CLI-English-Dictionary/blob/main/word_of_the_day.png)
## Words with pagination
![Main menu](https://github.com/Iguinho94CP/CLI-English-Dictionary/blob/main/words.png)
## Full description of the word's meaning
![Main menu](https://github.com/Iguinho94CP/CLI-English-Dictionary/blob/main/full_description.png)
## Submenu with options to UPDATE & DELETE & Go back
![Main menu](https://github.com/Iguinho94CP/CLI-English-Dictionary/blob/main/submenu.png)


## Usage

To use the MyDict application, follow these steps:

1. Run the application by executing the following command:

   ```bash
   python main.py
   ```

   The application will display a menu with options to perform various tasks:
   - **Add a word:** Add a new word along with its meaning and related information.
   - **Word of the day:** Display the word of the day along with its meaning.
   - **Show words:** Display a list of words stored in the database.
   - **Exit:** Close the application.

2. Choose an option by entering the corresponding number and following the prompts.

## Features

- **Add a Word:** Add new words to the database with their meanings. The application uses an external API to fetch meanings if available.

- **Word of the Day:** Retrieve and display the word of the day along with its meaning. The application also allows you to add the word of the day to the database.

- **Show Words:** Display a list of words stored in the database. You can navigate through the list, view brief descriptions, and access more details about each word.

- **Update and Delete:** For each word displayed, you can access a submenu to update or delete the word's information.

## Note

- The application uses external APIs and web scrapers to gather data, so an active internet connection is required.

- The application provides a user-friendly text-based interface for interacting with words and their details.

- The code is well-documented and organized into classes and methods for easy understanding and maintenance.
  
## TODO

- [ ] Integrate the thesaurus scraper to the main.py class
- [ ] Implement vocabulary trainer
- [ ] Implement vocabulary quizzes
- [ ] Implement the UPDATE & DELETE methods
- [ ] Implement search functionality

## Credits

This application was developed by [Igor Pantaleão](https://www.linkedin.com/in/igor-pantaleao)
