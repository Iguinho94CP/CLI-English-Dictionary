from app.main import MyDict
from app.database import Database

if __name__ == "__main__":
    database = Database("sqlite:///mydict.db")
    database.create_tables()  # Create the necessary tables
    app = MyDict(database)
    app.menu()
