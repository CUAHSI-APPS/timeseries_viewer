from .model import engine, SessionMaker, Base, URL,rscript,engine1,SessionMaker1,Base1

def init_urls_db():
    """
    An example persistent store initializer function
    """
    # Create tables
    Base.metadata.create_all(engine)

def init_rscript_db():
    Base1.metadata.create_all(engine1)