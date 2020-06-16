from bs4 import BeautifulSoup
from requests import get
from time import sleep
from utils import extract_pronunciation

WORD_REFERENCE = "https://www.wordreference.com/definition/"

prompt_input = input("Enter key for search: \n")

if prompt_input is None:
    print("key for search is required")
    exit(1)

keys = prompt_input.split(" ")
print(f"input value {keys}\n")
pronunciations = []

for key in keys:
    url_request = "{}{}".format(WORD_REFERENCE, key.lower().replace("’", "'"))
    print(f"URL for search {url_request}\n")
    pronunciation = extract_pronunciation(url_request)
    pronunciations.append(pronunciation)
    sleep(1.5)

phrase = ""
for index in range(len(keys)):
    phrase += pronunciations[index] + " "

print("Pronunciation: \n")
print(phrase)
