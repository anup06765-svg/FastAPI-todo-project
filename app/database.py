from sqlalchemy import create_engine #create_engine() database ke saath connection banata hai.
from sqlalchemy.orm import sessionmaker #Session database se baat karne ke liye use hota hai. jaise ki data ko ,insert,read, write, update karna.
from sqlalchemy.orm import declarative_base #Ye database tables banane ke liye base class hai.

# SQLite database ka path
DATABASE_URL = "sqlite:///./todo.db"

# Database engine create karna
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class
Base = declarative_base()

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()