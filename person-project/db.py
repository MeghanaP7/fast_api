from databases import Database

DATABASE_URL = "sqlite:///person.db"
database = Database(DATABASE_URL)

def get_database() -> Database:
    return database
