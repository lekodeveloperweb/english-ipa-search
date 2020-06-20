from requests import get
from bs4 import BeautifulSoup
from utils import find, trim, validate_url
from time import sleep
from .model import PronunciationModel, WordReferencesModel

WORD_REFERENCE = "https://www.wordreference.com/"
WORD_REFERENCE_DEFINITION = f"{WORD_REFERENCE}definition/"
WORD_REFERENCE_SYNONYMS = f"{WORD_REFERENCE}synonyms/"
WORD_REFERENCE_USAGE = f"{WORD_REFERENCE}EnglishUsage/"
WORD_REFERENCE_COLLOCATIONS = f"{WORD_REFERENCE}EnglishCollocations/"
WORD_REFERENCE_CONJUG = f"{WORD_REFERENCE}conj/enverbs.aspx?v="


class WordReferences:

    def __init__(self, words, source=None):
        self._selected_search_type = self.get_search_types()["DEFINITION"]
        self._words = words.split(" ")
        if len(self._words) == 1:
            url_source = self._get_url_source(self._selected_search_type)
            print(url_source)
            self._create_bs4_instance(url_source + self._words[0])

    def get_search_types(self):
        return {
            "DEFINITION": 1,
            "SYNONYMS": 2,
            "USAGE": 3,
            "COLLOCATIONS": 4,
            "CONJUG": 5,
        }

    def _get_url_source(self, key):
        sources = {
            1: WORD_REFERENCE_DEFINITION,
            2: WORD_REFERENCE_SYNONYMS,
            3: WORD_REFERENCE_USAGE,
            4: WORD_REFERENCE_COLLOCATIONS,
            5: WORD_REFERENCE_CONJUG,
        }
        return sources[key]

    def set_search_type(self, search_type):
        types = self.get_search_types()
        search = types[int(search_type)]
        if search == None:
            print(f"invalid type {search_type}")
            exit(1)
        self._selected_search_type = search

    def _get_content_from_web(self, url):
        response = get(url)
        if response.status_code != 200:
            raise Exception(f"Error on get resource from web {url}")
        return response

    def _create_bs4_instance(self, source):
        is_url = validate_url(source)
        if is_url == True:
            content = self._get_content_from_web(source)
            source = content.text

        self.html = BeautifulSoup(source, "html.parser")

    def extract_pronunciation(self):
        print("Pronunciation:\n")
        print(self._words)
        print(self._selected_search_type)
