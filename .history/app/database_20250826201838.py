from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# connect
DATABASE_URL = "mysql+pymysql://QuocDat:17122005@127.0.0.1:3306/fruit_store"

# tạo engine
engine = create_engine