from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'todos.db'}"
#DATABASE_URL = 'postgresql://postgres:0000@localhost/TodoApplicationDatabase'
#DATABASE_URL = 'mysql+pymysql://root:0000@127.0.0.1:3307/TodoApplicationDatabase'

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
#engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from ..entities.todo import Todo  # Ensure model metadata is registered before create_all.
    from ..entities.user import User

    Base.metadata.create_all(bind=engine)

