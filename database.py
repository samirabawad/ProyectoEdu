from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:12345@localhost:3306/dbEdu2"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

#argumendo ccheck same thread, es solo necesitado en sqlite. Esto asegura que cada request...
#...tiene su propia sesion de conexion a base de datos en una dependencia.
engine = create_engine(DATABASE_URL)
#cada instancia es una sesion en la bd.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#se ocupara para crear cada clase de la bd en models.py
Base= declarative_base()