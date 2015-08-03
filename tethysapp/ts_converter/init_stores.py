from .model import engine, SessionMaker, Base, URL

def init_urls_db():
    """
    An example persistent store initializer function
    """
    # Create tables
    Base.metadata.create_all(engine)

