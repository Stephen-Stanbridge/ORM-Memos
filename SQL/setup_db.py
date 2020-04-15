from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db_strings import DEV_DB_STR, PROD_DB_STR


DB = 'prod'
if DB == 'prod':
    engine = create_engine(PROD_DB_STR, echo=False)
elif DB == 'dev':
    engine = create_engine(DEV_DB_STR, echo=False)


Session = sessionmaker(bind=engine)
