from sqlalchemy import create_engine

from config import CONNECTION_STRING

engine = create_engine(CONNECTION_STRING, echo=True)
