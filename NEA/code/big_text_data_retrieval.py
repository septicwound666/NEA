#import regex library
import re

# Read Sherlock Holmes.txt and store as big text
big_text = open("C:\\Users\\User\\Desktop\\NEA\\data\\sherlock_holmes.txt", "r")

#Split big_text into separate words
imported_text = []
total_words = 0
for line in big_text:
	for word in line.split():
		total_words += 1
		#Use a regular expression to remove punctuation 
		word = re.sub(r'[^\w\s]', " ",word)
		#Splits hyphenated words to single words
		phrase = word.split(" ")
		for i in phrase:
			#Create a list of words
			imported_text.append(i.lower())
print(imported_text)

#Convert list into a dictionary with frequencies
words = {}
for i in imported_text:
	if i in words.keys():
		words[i] += 1
	else:
		words[i] = 1

#Create decimal probability from frequencies
for i in words:
	words[i] = (words[i] / total_words)
print(words)

#write probabilities to document for later use in main program
writer = open("C:\\Users\\User\\Desktop\\NEA\\data\\sherlock_probs.txt", "a")
writer.write(str(words))

#test reading the file and converting it back to a dictionary
reader = open('C:\\Users\\User\\Desktop\\NEA\\data\\sherlock_probs.txt', 'r').read()
words_mk2 = eval(reader)

print(words_mk2)