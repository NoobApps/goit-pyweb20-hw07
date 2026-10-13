import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from random import randint

engine = create_engine("postgresql+psycopg2://postgres:example@localhost/postgres", echo=False)
Session = sessionmaker(engine)
session = Session()
