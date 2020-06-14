from bs4 import BeautifulSoup
from requests import get
from time import sleep
from subprocess import run

WORD_REFERENCE = "https://www.wordreference.com/definition/"


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def extract_pronunciation(url_request):
    response = get(url_request)
    if response.status_code is not 200:
        print(f"Error on get page content {response.status_code}")
        exit(1)

    html_soup = BeautifulSoup(response.text, "html.parser")
    isp = html_soup.find("div", class_="pwrapper")
    tag_pron = isp.find("span", class_="pronWR")
    if tag_pron is None:
        return "(No UK ISP)"
    pronun_values = tag_pron.text
    indexs = find(pronun_values, "/")

    if len(indexs) == 0:
        print("Pronunciation ISP not found")
        exit()
    # 36 length to phrase "UK and possibly other pronunciations"
    pronunciation = pronun_values[36:]
    return pronunciation


prompt_input = input("Enter key for search: \n")

if prompt_input is None:
    print("key for search is required")
    exit(1)

keys = prompt_input.split(" ")
print(f"input value {keys}\n")
pronunciations = []

for key in keys:
    url_request = WORD_REFERENCE + key.lower().replace("’", "'")
    print(f"URL for search {url_request}\n")
    pronunciation = extract_pronunciation(url_request)
    pronunciations.append(pronunciation)
    sleep(1.5)

phrase = ""
for index in range(len(keys)):
    phrase += pronunciations[index] + " "

print("Pronunciation: \n")
print(phrase)
print("\n")
run("pbcopy", universal_newlines=True, input=phrase)
print("Phrase copied to clipboard 🍻🎉")
