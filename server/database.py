#OLD WAY TO INITIALIZE DB, NOT USING FLASK-SQLALCHEMY
#WITH THAT METHOD, MODELS INHERIT FROM Base, AND NOT db.Model

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import os

#Config, prepare the connection, no file created there
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "db", "app.db")
engine = create_engine(f'sqlite:///{db_path}')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()

#Allow the use of query
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import server.models

    #Look at registered models and issue CREATE TABLE
    Base.metadata.create_all(bind=engine)