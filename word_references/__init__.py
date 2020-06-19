from requests import get
from bs4 import BeautifulSoup
from utils import find, trim
from time import sleep

WORD_REFERENCE = "https://www.wordreference.com/definition/"


class Pronunciation(object):

    def __init__(self, pronunciation=None, type_pronun=None):
        self.type_pronun = type_pronun
        self.pronunciation = pronunciation


class WordReferencesModel(object):

    def __init__(self):
        self.word = ""
        self.audios = []
        self.pronunciation = None
        self.sentences = []


class WordReferences:

    def __init__(self, input_term, source=None):
        if input_term is None or input_term == "":
            raise Exception("term for search is required")

        terms = input_term.split(" ")
        self.words = []
        self._pronunciations = []
        self._html_soup = None
        for term in terms:
            word = trim(term)
            if(word != None and word != ""):
                self.words.append(word)

        self.source = source

    def _get_by_url(self, url):
        response = get(url)
        if response.status_code != 200:
            raise Exception(
                f"Error on get page content {response.status_code}")

        return response

    def _extract_from_html(self, content):
        self._html_soup = BeautifulSoup(content, "html.parser")
        isp = self._html_soup.find("div", class_="pwrapper")
        tag_pron = isp.find("span", class_="pronWR")
        if tag_pron is None:
            return "(No UK ISP)"
        pronun_values = tag_pron.text
        indexs = find(pronun_values, "/")

        if len(indexs) == 0:
            print("Pronunciation ISP not found")
            exit()
        # 36 length to phrase "UK and possibly other pronunciations"
        return pronun_values[36:]

    def print_formatted(self):
        phrase = ""
        for index in range(len(self.words)):
            phrase += self._pronunciations[index].pronunciation.pronunciation + " "
        print(phrase)

    def extract_pronunciation(self):
        response = {'text':  self.source}
        for word in self.words:
            url_request = "{}{}".format(WORD_REFERENCE, word)
            print(f"URL for search {url_request}\n")
            if(self.source is None):
                response = self._get_by_url(url_request)

            model = WordReferencesModel()
            pronunciation = self._extract_from_html(response.text)

            h3_tag = self._html_soup.find("h3", class_="headerWord")
            audios = self._html_soup.findAll("audio")
            for audio in audios:
                source = audio.source
                audio_url = source.get("src")
                model.audios.append(audio_url)
            model.word = h3_tag.text

            model.pronunciation = Pronunciation(pronunciation, "all")
            self._pronunciations.append(model)
            sleep(1.5)

        return self._pronunciations
