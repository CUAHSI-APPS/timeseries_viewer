from .model import engine, Base,engine1,Base1

def init_urls_db(first_time):
    """
    An example persistent store initializer function
    """
    # Create tables
    Base.metadata.create_all(engine)

def init_rscript_db(first_time):
    Base1.metadata.create_all(engine1)