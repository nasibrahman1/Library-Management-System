from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def create_db_engine():
    engine = None
    print("Trying to creat db engine...")
    try:
        db_url = "sqlite:///library_db.db"
        engine = create_engine(db_url)
        print("DB engine created successfully")
    except Exception as e:
        print("Error while creating db engine")
        print(e)    
    finally:
        return engine
    
def create_session(engine):
    session = None
    print("trying to create session...")
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        print("Session created successfully")
    except Exception as e:
        print("Error while trying to create session")
        print(e)
    
    finally:
        return session
    
    