import datetime

from sqlalchemy import create_engine, Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///sqlite3.db', connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)

Base = declarative_base()


class WordsTable(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)

    word = Column(String(50), nullable=False)
    translation = Column(String(50), nullable=False)

    lesson_name = Column(String(50), ForeignKey("lessons.name"), nullable=False)

    def __repr__(self):
        return f"word: {self.english}, translation: {self.translation}"


class LessonsTable(Base):
    __tablename__ = 'lessons'
    name = Column(String(50), primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"Lesson {self.name}, {self.datetime}"


Base.metadata.create_all(engine)
