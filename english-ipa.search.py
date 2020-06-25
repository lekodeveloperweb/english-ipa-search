from word_references import WordReferences

prompt_input = input("Enter key for search: \n")

service = WordReferences(prompt_input)
service.print_option()
prompt_input = input()
pronunciations = service.extract_pronunciation(prompt_input)
for pron in pronunciations:
    print(f"{pron.type_pronun} {pron.pronounce}")
