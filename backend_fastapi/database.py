import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

MYSQL_USER = os.environ.get("MYSQL_USER", "payment_user")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "payment_pass")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "mysql")
MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "payment_system")

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# FastAPI shares the same MySQL database that Django's migrations create
# and manage. Django owns the schema (Module 7); this service only reads
# and writes rows through SQLAlchemy Core-mapped models pointed at
# Django's existing table names ("cards_card", "transactions_transaction").
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
