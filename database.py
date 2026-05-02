import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker   


# Load environment variables
load_dotenv()

try:
    # Get DATABASE_URL from .env
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not found in .env file")

    print("Connecting to database...")

    # Create engine
    engine = create_engine(DATABASE_URL)

    # Connect to database
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()

        print("DB Connected Successfully!")
        print("Database Version:", version[0])

except Exception as e:
    print("Error connecting to the database:")
    print(e)




# engine 
engine = create_engine( DATABASE_URL)

# session
Session = sessionmaker(bind = engine)

# dependency
def get_db():
    db = Session()
    try:
        yield db     #Generator Function
    finally:
        db.close()    #always close the session or database connection after use3