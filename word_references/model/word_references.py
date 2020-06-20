from . import PronunciationModel


class WordReferencesModel:

    def __init__(self):
        self.word = ""
        self.audios = []
        self.pronunciation = PronunciationModel()
        self.sentences = []
