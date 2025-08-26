from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# connect
DATABASE_URL = "mysql+pymysql://QuocDat:17122005@127.0.0.1:3306/fruit_store"

# tạo engine
engine = create_engine(DATABASE_URL, echo=True)


# Tạo session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho ORM
Base = declarative_base()

# Dependency: mỗi request có 1 session riêng
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()