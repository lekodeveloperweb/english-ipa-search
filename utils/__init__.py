import re

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def trim(s):
    return s.lower().replace("’", "'").replace(".", "").replace(",","")

def validate_url(source):
    regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, source) != None


