from word_references import WordReferences
from csv import DictReader


def read_from_word_or_sentence(word=None):
    if word != None:
        word = word.strip()
    prompt_input = word
    if prompt_input == None:
        prompt_input = input("Enter key for search: \n")
    service = WordReferences(prompt_input)
    prompt_input = 1
    if word == None:
        service.print_option()
        prompt_input = input()
    pronunciations = service.extract_pronunciation(prompt_input)
    pronunciation = ""
    for pron in pronunciations:
        if type(pron) == list:
            pronunciation += f"{pron[1].pronounce} "
            print(
                f"WORD: {pron[1].word}\nTYPE: {pron[1].type_pronun}\nPRONOUNCE: {pron[1].pronounce}\n")
        else:
            pronunciation += f"{pron.pronounce} "
            print(
                f"WORD: {pron.word}\nTYPE: {pron.type_pronun}\nPRONOUNCE: {pron.pronounce}\n")

    print(f"{pronunciation}\n")


def read_from_csv_file(path, dict_key, start=0, end=None, delimiter="\t"):
    with open(path, newline="") as csvFile:
        wordReader = DictReader(csvFile, delimiter=delimiter)
        rows = list(wordReader)
        if end != None:
            rows = rows[start:end if len(rows) > end else len(rows) - 1]
        else:
            rows = rows[start:]
        for row in rows:
            read_from_word_or_sentence(row[dict_key])


print("Choose an option:\n")
print("\t1 - Write de word or sentence")
print("\t2 - Read from csv file")
response = input()
print()

if response == "1":
    read_from_word_or_sentence()
else:
    path = input("Write path to csv/tsv file: ")
    dict_key = input("What is the dic key? ")
    start = input("Start read from...(index of row. Default 1): ")
    if start == '':
        start = 1
    end = input("Read at... (index of end row. Default None): ")
    delimiter = input("Delimiter... (Default \\t): ")
    print()
    if delimiter == '':
        delimiter = '\t'
    read_from_csv_file(path, dict_key, int(start), int(end), delimiter)
