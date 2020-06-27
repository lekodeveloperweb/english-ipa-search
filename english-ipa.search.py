from word_references import WordReferences

prompt_input = input("Enter key for search: \n")

service = WordReferences(prompt_input)
service.print_option()
prompt_input = input()
pronunciations = service.extract_pronunciation(prompt_input)
# print(pronunciations)
pronunciation = ""
for pron in pronunciations:
    if type(pron) == list:
        pronunciation += f"{pron[1].pronounce} "
        print(
            f"WORD: {pron[1].word}\nTYPE: {pron[1].type_pronun}\n\n{pron[1].pronounce}\n")
    else:
        pronunciation += f"{pron.pronounce} "
        print(
            f"WORD: {pron.word}\nTYPE: {pron.type_pronun}\n\n{pron.pronounce}\n")

print(pronunciation)
