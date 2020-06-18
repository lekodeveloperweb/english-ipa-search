from word_references import WordReferences

prompt_input = input("Enter key for search: \n")

service = WordReferences(prompt_input)
service.extract_pronunciation()

print("Pronunciation: \n")
service.print_formatted()
print("\n")
