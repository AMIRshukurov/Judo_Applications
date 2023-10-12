from sqlalchemy import Column,String,VARCHAR, BIGINT
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from dotenv import load_dotenv

load_dotenv()
ip = os.getenv("ip")
DB_USER = os.getenv('db_user')
DB_PASS = os.getenv('db_pass')
DB_NAME = os.getenv('db_name')
port = os.getenv("port")

POSTGRES_URI = f'postgresql://{DB_USER}:{DB_PASS}@{ip}:{port}/{DB_NAME}'
engine = create_engine(POSTGRES_URI)

Base = declarative_base()


class Application(Base):
    __tablename__ = 'applications'

    application_id = Column(String, unique=True, nullable=False, primary_key=True)
    user_id = Column(String, unique=True, nullable=False)
    surname = Column(String)
    name = Column(String)
    weight = Column(VARCHAR)
    contact = Column(String)
    photo = Column(String)


class Language(Base):
    __tablename__ = "user_lang"
    user_id = Column(BIGINT, unique=True, nullable=False, primary_key=True)
    lang = Column(String, default="eng")


Session = sessionmaker(bind=engine)
session = Session()


def save_lang(user_id, lang):
    app = Language(user_id=user_id, lang=lang)
    session.add(app)
    session.comit()
    session.close()


def save_application(user_id, name, surname, weight, contact, photo, application_id):
    app = Application(user_id=user_id, name=name, surname=surname, weight=weight, contact=contact, photo=photo,
                      application_id=application_id)
    session.add(app)
    session.commit()
    session.close()


def check_user_exists(user_id):
    try:
        session.query(Application).filter_by(user_id=user_id).one()
        exists = True
    except NoResultFound:
        exists = False
    return exists


def chek_lang(user_id):
    try:
        session.query(Language).filter_by(user_id=user_id).one()
        exists = user_id
    except NoResultFound:
        exists = False
    return exists


Base.metadata.create_all(engine)

