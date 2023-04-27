from typing import Optional

from telebot import TeleBot, types

from src.adapter import Adapter
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
        self._edit_lesson.add_word(lines[1].lower().strip(), lines[2].lower().strip())
        self._edit_lesson.save()

    def add_lesson(self, msg: types.Message):
        lines = msg.text.split('\n')
        if len(lines) < 2:
            return

        self._run_lesson = None
        self._edit_lesson = Lesson(lines[1])
        self._edit_lesson.save()

    def start_lesson(self, msg: types.Message):
        lines = msg.text.split('\n')
        if len(lines) < 2:
            return
        if self._edit_lesson is not None:
            self._edit_lesson.save()
            self._edit_lesson = None
        self._run_lesson = Lesson.load_from_db(lines[1])
        self._bot.send_message(text=f"Lesson {self._run_lesson.name} start", chat_id=msg.chat.id)
        word, _ = self._run_lesson.get_next_word()
        if word is None:
            self._bot.send_message(text=f'Lesson is empty, add words.', chat_id=msg.chat.id)
            return
        self._bot.send_message(text=f'Translate it into Russian: \n{word}', chat_id=msg.chat.id)

    def list_lesson(self, msg: types.Message):
        lessons = Adapter().list_lesson()
        text = 'Lessons: \n' + '\n'.join(f"{lesson[0]}, {lesson[1]}" for lesson in lessons)
        self._bot.send_message(text=text, chat_id=msg.chat.id)

    def text_command(self, msg: types.Message):
        if self._run_lesson is None:
            return
        _, translation = self._run_lesson.get_next_word()
        ueser_translation = msg.text.lower().strip()
        if ueser_translation != translation:
            self._bot.reply_to(msg, 'Wrong answer')
        else:
            self._bot.reply_to(msg, 'Correct')
            word, _ = self._run_lesson.get_next_word(passed=True)
            if word is None:
                self._bot.send_message(text=f'Lesson is complete, choose another lesson.', chat_id=msg.chat.id)
                return
            self._bot.send_message(text=f'Translate it into Russian: \n {word}', chat_id=msg.chat.id)

