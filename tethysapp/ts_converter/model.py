from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float,String
from sqlalchemy.orm import sessionmaker

from .utilities import get_persistent_store_engine

# DB Engine, sessionmaker and base
engine = get_persistent_store_engine('urls_db')
SessionMaker = sessionmaker(bind=engine)
Base = declarative_base()

class URL(Base):
    '''
    Example SQLAlchemy DB Model
    '''
    __tablename__ = 'urls'

    # Columns
    id = Column(Integer, primary_key=True)
    url = Column(String)

    def __init__(self, url):
        """
        Constructor for a gage
        """
        self.url = url


  # DB Engine, sessionmaker and base
engine1 = get_persistent_store_engine('rscript_db')
SessionMaker1 = sessionmaker(bind=engine1)
Base1 = declarative_base()

class rscript(Base1):
    '''
    Example SQLAlchemy DB Model
    '''
    __tablename__ = 'R Scripts'

    # Columns
    id = Column(Integer, primary_key=True)
    rscript = Column(String)

    def __init__(self, rscript):
        """
        Constructor for a gage
        """
        self.rscript = rscript