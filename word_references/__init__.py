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
        if words == None or len(words) == 0:
            raise AttributeError("Property [words] is required")

        self._words = []
        for w in words.split(" "):
            if trim(w) != None:
                self._words.append(w)

    def get_search_types(self):
        return {
            1: "DEFINITION",
            2: "SYNONYMS",
            3: "USAGE",
            4: "COLLOCATIONS",
            5: "CONJUG",
        }

    def print_option(self):
        types = self.get_search_types()
        print("\nSelect an options:")
        for t in types:
            print(f"\t {t} for {types[t]}")

    def _get_url_source(self, key):
        sources = {
            "DEFINITION": WORD_REFERENCE_DEFINITION,
            "SYNONYMS": WORD_REFERENCE_SYNONYMS,
            "USAGE": WORD_REFERENCE_USAGE,
            "COLLOCATIONS": WORD_REFERENCE_COLLOCATIONS,
            "CONJUG": WORD_REFERENCE_CONJUG,
        }
        return sources[key]

    def _get_function_by_type(self, key):
        sources = {
            "DEFINITION": self._extract_definition,
            "SYNONYMS": self._extract_definition,
            "USAGE": self._extract_definition,
            "COLLOCATIONS": self._extract_definition,
            "CONJUG": self._extract_definition,
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

    def _extract_types(self, text):
        if "strong" not in text:
            return [PronunciationModel(text)]
        text_split = text.split(",")
        pronounces = []
        for word in text_split:
            splits = word.split(":")
            pronounces.append(PronunciationModel(
                splits[1].strip(), splits[0].strip()))
        return pronounces

    def _extract_definition(self):
        isp = self.html.find("div", class_="pwrapper")
        tag_pron = isp.find("span", class_="pronWR")
        if tag_pron is None:
            return "(No UK ISP)"
        pronun_values = tag_pron.text
        indexs = find(pronun_values, "/")

        if len(indexs) == 0:
            print("Pronunciation ISP not found")
            exit()
        # 36 length to phrase "UK and possibly other pronunciations"
        return self._extract_types(pronun_values[36:])

    def _extract_by_type(self):
        function = self._get_function_by_type(self._selected_search_type)
        return function()

    def extract_pronunciation(self, search_type):
        if search_type == None:
            raise AttributeError("[search_type] is required")

        search_type = int(search_type)
        if search_type < 1 or search_type > 5:
            raise AttributeError("Invalid option")

        self._selected_search_type = self.get_search_types()[search_type]

        if len(self._words) == 1:
            url_source = self._get_url_source(self._selected_search_type)
            self._create_bs4_instance(url_source + self._words[0])
            pronunciation = self._extract_by_type()
            return pronunciation
