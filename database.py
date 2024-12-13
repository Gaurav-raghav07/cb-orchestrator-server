from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
# Declare Base Class
Base = declarative_base()

class DatabaseToSQL:

    def __init__(self) -> None:
        # SQL Server connection parameters
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_PORT = os.getenv("DB_PORT")
    
    def create_engine_connection(self):
        print("Attempting to establish a database connection.")

        try:
            # Create a connection URL
            connection_url = sqlalchemy.engine.URL.create(
                drivername="mysql+pymysql",
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT,
                database=self.DB_NAME,
            )

            # Create engine with connection URL
            engine = create_engine(connection_url)
            
            return engine
        
        except Exception as e:
            print(f"Error establishing database connection: {e}")
            return None, None

dbObj = DatabaseToSQL()
engine  = dbObj.create_engine_connection()        

def get_db():
    

    # Create a session
    Session = sessionmaker(bind=engine,autoflush=False, autocommit=False)
    session = Session()

    try: 
        yield session
    finally: 
        session.close()
    
    