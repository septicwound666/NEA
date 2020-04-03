#import regular expressions library and the lancaster stemmer object
import re
from nltk.stem.lancaster import LancasterStemmer
lancaster = LancasterStemmer()

#turn insignificant_words into a list of words
insignificant_words = open("C:\\Users\\User\\Desktop\\NEA\\data\\insignificant.txt", "r")
insignificant = []
lines = insignificant_words.readlines()
insignificant = lines[0].split()

#create class for preprocessing of text
class preprocessing(object):
	def __init__(self, user):
		self.user = user

	#define tokenization function
	def tokenizer(self, text):
		#reg ex to remove words containing apostrophes or hyphens
		word = re.sub(r"('\w+|\w+'\w+|\w+'|'|\w+-\w+)",r"",text)
		word = word.split()
		clean_list = []
		for i in range(0,len(word)):
			#remove whitespace leftover from regex removal
			word[i] = word[i].strip()
			#append linguistically significant words to clean_list
			if word[i].lower() not in insignificant:
				clean_list.append(word[i])
		return (clean_list)

	#define lemmatization function
	def lemmatizer(self, text):
		broken = text.split()
		stemmed = []
		for i in broken:
			stemmed.append(lancaster.stem(i))
		return(stemmed)

#define main function to get user input and tokenize and lemmatize text
def main():
	text = preprocessing(input("User Input Text Goes Here!!!:  "))
	tokenized = text.tokenizer(text.user)
	lemmatized = text.lemmatizer(text.user)
	return(text.user,tokenized,lemmatized)

