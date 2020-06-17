from word_references import WordReference

prompt_input = input("Enter key for search: \n")

service = WordReference(prompt_input)
service.extract_pronunciation()

print("Pronunciation: \n")
service.print_formatted()
print("\n")
