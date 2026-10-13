import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "example")
DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "postgres")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}", echo=False)
Session = sessionmaker(engine)
session = Session()
