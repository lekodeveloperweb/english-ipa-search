from requests import get
from bs4 import BeautifulSoup

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def extract_pronunciation(url_request):
    response = get(url_request)
    if response.status_code != 200:
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

