from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

DATABASE_URL = config.mySqlConnectionString

engine = create_engine(DATABASE_URL)
makeSession=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()