from nltk.corpus import words
#d = enchant.Dict("en_GB")

#checker = d.check("Hello")
checker = None
if "Insert Word to be checked here" in words.words():
	checker = True
else:
	print("N A H")
print(str(checker))