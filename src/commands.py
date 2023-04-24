from typing import Optional

from telebot import TeleBot, types

from src.lesson import Lesson


class Commands:
    def __init__(self, bot: TeleBot):
        self._bot = bot

        self._run_lesson: Optional[Lesson] = None
        self._edit_lesson: Optional[Lesson] = None

    def add_word(self, msg: types.Message):
        if self._edit_lesson is None:
            return
        lines = msg.text.split('\n')
        self._edit_lesson.add_word(lines[1], lines[2])
        self._edit_lesson.save()

    def add_lesson(self, msg: types.Message):
        lines = msg.text.split('\n')
        if len(lines) < 2:
            return

        self._run_lesson = None
        self._edit_lesson = Lesson(lines[1])
        self._edit_lesson.save()

    def start_lesson(self, msg: types.Message):
        pass

    def list_lesson(self, msg: types.Message):
        pass

    def text_command(self, msg: types.Message):
        pass
