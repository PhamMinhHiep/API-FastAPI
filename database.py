from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# string refer to DB
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:phamhiep1312@localhost:3306/restapi"

# create connection  to local database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, encoding = 'UTF-8', echo = True
)

#SessionLocal is a Session object
#autocommit: setting to use with newly created Session objects
#autoflush: setting to use with newly created Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# callable return a new base class from which all mapped classes should inherit.
# when the class definition is completed, a new Table amd mapped will have generated.
Base = declarative_base()


