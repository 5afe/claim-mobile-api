import sqlalchemy as sqlalchemy
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

DB_URL = "sqlite:///./db.db"

engine = sqlalchemy.create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()


def create_db():
    return Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
