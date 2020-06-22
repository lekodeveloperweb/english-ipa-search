from word_references import WordReferences

prompt_input = input("Enter key for search: \n")

service = WordReferences(prompt_input)
service.print_option()
prompt_input = input()
service.extract_pronunciation(prompt_input)
