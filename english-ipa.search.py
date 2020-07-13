from word_references import WordReferences
from csv import DictReader
from clipboard import copy


export_result = False
pronunciation_list = []
debug_mode = True


def read_from_word_or_sentence(word=None):
    if word != None:
        word = word.strip()
    prompt_input = word
    if prompt_input == None:
        prompt_input = input("Enter key for search: \n")
    service = WordReferences(prompt_input)
    prompt_input = "1"
    if word == None:
        service.print_option()
        prompt_input = input()
    pronunciations = service.extract_pronunciation(prompt_input)
    pronunciation = ""
    for pron in pronunciations:
        if type(pron) == list:
            pronunciation += f"{pron[1].pronounce} "
            if debug_mode:
                print(
                    f"WORD: {pron[1].word}\nTYPE: {pron[1].type_pronun}\nPRONOUNCE: {pron[1].pronounce}\n")
        else:
            pronunciation += f"{pron.pronounce} "
            if debug_mode:
                print(
                    f"WORD: {pron.word}\nTYPE: {pron.type_pronun}\nPRONOUNCE: {pron.pronounce}\n")

    if export_result:
        pronunciation_list.append(pronunciation)
    else:
        copy(pronunciation)
        print("copied to clipboard!")

    if debug_mode:
        print(f"{pronunciation}\n")


def read_from_csv_file(path, dict_key, start=0, end=None, delimiter=","):
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
    path = input("Write path to csv/tsv file: ").strip()
    dict_key = input("What is the dic key? ").strip()
    start = input("Start read from...(index of row. Default 0): ").strip()
    if start == '':
        start = 0
    end = input("Read at... (index of end row. Default None): ").strip()
    if end == '':
        end = None
    delimiter = input("Delimiter... (Default \\,): ").strip()
    if delimiter == '':
        delimiter = ','
    response = input("Export result? [y/N]: ").strip()
    if response.lower() == 'y':
        export_result = True
    result = input("Debug mode? (Show results on console) [Y/n]: ").strip()
    if result.lower() == 'n':
        debug_mode = False
    print()

    read_from_csv_file(
        path,
        dict_key,
        int(start),
        int(end) if end != None else None,
        delimiter
    )

    if export_result:
        with open('data/export_result.txt', mode="w") as fileResult:
            for pronounce in pronunciation_list:
                fileResult.write(f"{pronounce}\n")
        print("\nresult exported with success!!! [data/export_result.txt]\n")
