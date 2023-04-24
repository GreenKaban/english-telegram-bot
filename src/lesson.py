from typing import Dict, Optional

from src.adapter import Adapter


class Lesson:
    def __init__(self, name, words: Optional[Dict[str, str]] = None):
        self.name = name

        self.words: Dict[str, str] = {} if words is None else words

    def add_word(self, word: str, translation: str):
        self.words[word] = translation

    def save(self):
        adp = Adapter()
        if not adp.exists_lesson(self.name):
            adp.add_lesson(self.name)

        for word, translation in self.words:
            adp.add_word(word, translation, self.name)

    @staticmethod
    def load_from_db(name_lesson):
        words = Adapter().get_words(name_lesson)
        return Lesson(name_lesson, words)
