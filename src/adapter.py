from datetime import datetime
from typing import Set, Optional, Iterable, Dict, List

from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker

from src.database import WordsTable, LessonsTable


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Adapter(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        engine = create_engine('sqlite:///sqlite3.db', connect_args={'check_same_thread': False})
        self.Session = sessionmaker(bind=engine)

    def add_word(self, word: str, translation: str, lesson_name: str):
        session = self.Session()
        session.add(WordsTable(word=word, translation=translation, lesson_name=lesson_name))
        session.commit()

    def add_lesson(self, lesson_name: str):
        session = self.Session()
        session.add(LessonsTable(name=lesson_name))
        session.commit()

    def get_words(self, lesson_name: str) -> Dict[str, str]:
        session = self.Session()
        query = session.query(WordsTable).filter(WordsTable.lesson_name == lesson_name).all()
        words = {word.word: word.translation for word in query}

        return words

    def exists_lesson(self, lesson_name) -> bool:
        session = self.Session()
        return session.query(LessonsTable.name).filter(LessonsTable.name == lesson_name).first() is not None

    def list_lesson(self):
        session = self.Session()
        return session.query(LessonsTable.name, LessonsTable.created_date).all()

        # def delete_plan(self, plan_id: int):
    #     session = self.Session()
    #     item = session.query(PlanModel).get(plan_id)
    #     session.delete(item)
    #     session.commit()
    #
    # def add_plan(self, plan: PlanModel, plan_id: Optional[int] = None) -> int:
    #     session = self.Session()
    #     if plan_id is not None:
    #         plan.id = plan_id
    #     session.add(plan)
    #     session.commit()
    #     session.refresh(plan)
    #     return plan.id
    #
    # def update_name(self, user_id: int, name: str):
    #     session = self.Session()
    #     user = session.query(UserModel).get(user_id)
    #     user.name = name
    #     session.add(user)
    #     session.commit()
    #

    #
    # def get_name(self, user_id: int) -> str:
    #     session = self.Session()
    #     user = session.query(UserModel).get(user_id)
    #     return user.name
