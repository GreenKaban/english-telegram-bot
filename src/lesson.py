import random
from typing import Dict, Optional

from src.adapter import Adapter


class Lesson:
    def __init__(self, name, words: Optional[Dict[str, str]] = None):
        self.name = name

        self.words: Dict[str, str] = {} if words is None else words

        self.active_words = list(self.words.keys())
        self.current_word = random.choice(self.active_words)

    def add_word(self, word: str, translation: str):
        self.words[word] = translation

    def save(self):
        adp = Adapter()
        if not adp.exists_lesson(self.name):
            adp.add_lesson(self.name)

        for word, translation in self.words.items():
            adp.add_word(word, translation, self.name)

    @staticmethod
    def load_from_db(name_lesson):
        words = Adapter().get_words(name_lesson)
        return Lesson(name_lesson, words)

    def get_next_word(self, passed=False) -> (str, str):
        if passed:
            self.active_words.remove(self.current_word)
            if len(self.active_words) == 0:
                return None, None
            self.current_word = random.choice(self.active_words)
        return self.current_word, self.words[self.current_word]

