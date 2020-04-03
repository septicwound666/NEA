#import the dictionary from the nltk regular expressions library, lancaster stemmer object, 
from nltk.corpus import words
import string
import re
from nltk.stem.lancaster import LancasterStemmer
lancaster = LancasterStemmer()

#turn insignificant_words doc into a list of words
insignificant_words = open("C:\\Users\\User\\Desktop\\NEA\\data\\insignificant.txt", "r")
insignificant = []
lines = insignificant_words.readlines()
insignificant = lines[0].split()

#get topic relevant words from document
topic_word_doc = open("C:\\Users\\User\\Desktop\\NEA\\data\\topic_1.txt", "r")
topic_words = topic_word_doc.readlines()
for i in range(0,len(topic_words)):
	topic_words[i] = topic_words[i].strip()
	topic_words[i] = topic_words[i].lower()

#create preprocessing class
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


#create processing class
class processing(object):
	def __init__(self,raw_text,tokenized,lemmatized,length_ideal):
		self.raw_text = raw_text
		self.tokenized = tokenized
		self.lemmatized = lemmatized
		self.length_ideal = length_ideal

	#define main function
	def main(self,raw_text,tokenized,lemmatized):
		#adjust stems to get words
		self.lemmatized = self.lemmatizer_adjust(self.lemmatized)
		#get length score
		length_value = str(self.length_check(raw_text))
		#get relevance score
		relevance_value = self.relevance_check()
		#spell check
		checked = self.spell_check(tokenized)
		#self.grammar()
		return(length_value)

	#define function to make lemmatized text into real word stems
	def lemmatizer_adjust(self,lemmatized):
		change = self.spell_check(lemmatized)
		if change == None:
			return(lemmatized)
		else:
			return(change)

	#define length checker function
	def length_check(self,raw_text):
		text_length = len(raw_text.split(" "))
		#calculate percentage difference from the ideal_length
		if text_length < self.length_ideal:
			percent_diff = (text_length/self.length_ideal)*100
		elif self.length_ideal < text_length:
			percent_diff = 100-(((text_length/self.length_ideal)-1)*100)
		else:
			percent_diff = 100
		return(str(percent_diff) + "%")

	#define relevance checker function
	def relevance_check(self):
		relevant = relevance_checking(self.lemmatized,None,None,None,None)
		relevant.bag_of_words()
		for word in relevant.bag_of_words.keys():
			TF, IDF = self.TF_IDF(word)

		"""
		vector = TF * IDF
		self.cosine_similarity(TF,IDF,vector)
		"""

	#define spell check main function to colect all edited and known words created
	def spell_check(self,checking):
		to_check = []
		#list to put the suggested edits into
		checked_sentence = checking
		#collect words that don't exist
		for word in checking:
			if word.lower() not in words.words():
				to_check.append(word)
		#iterate over non-existent words
		if len(to_check) > 0:
			for word in to_check:
				#perform single letter edits
				spelling = spell_checking(word)
				print("start spell check on " + str(word))
				deletes_known, deletes_all = spelling.deletes(1,None,spelling.checking)
				#print("deletes_done")
				transposes_known, transposes_all = spelling.transposes(1,None,spelling.checking)
				#print("transposes_done")
				replaces_known, replaces_all = spelling.replaces(1,None,spelling.checking)
				#print("replaces_done")
				inserts_known, inserts_all = spelling.inserts(1,None,spelling.checking)
				#print("inserts_done")
				#collect words that exist created by single letter edits and all edited strings for secondary letters edits
				word_known = deletes_known + transposes_known + replaces_known + inserts_known
				greatest = spelling.spelling_probs(word_known)
				if greatest[0] != None:
					print("The most likely replacement for " + str(word) + " was " + greatest[0] + " with a probability value of " + str(greatest[1]))
					for i in range(0,len(checked_sentence)):
						if checked_sentence[i] == word:
							checked_sentence[i] = greatest[0]
				else:
					print("Word had no possible alternatives")
				#SECONDARY EDITS CODE REMOVED DUE TO VERY LARGE RUN TIME
				"""
				words_all = deletes_all + transposes_all + replaces_all + inserts_all
				
				#iterate over the single letter edited words and perform the secondary letter edits
				word_known_2 = []
				for i in range(0,len(words_all)):
					deletes_known_2 = spelling.deletes(2,words_all[i],None)
					transposes_known_2 = spelling.transposes(2,words_all[i],None)
					replaces_known_2 = spelling.replaces(2,words_all[i],None)
					inserts_known_2 = spelling.inserts(2,words_all[i],None)
					word_known_2 += deletes_known_2 + transposes_known_2 + replaces_known_2 + inserts_known_2
				#spelling.spelling_probs(word_known)
				"""
			return(checked_sentence)
		print("words all exist")
		return(None)

	def grammar_check(self):
		pass

	def two_sided_check(self):
		pass


#create class for relevance checking
class relevance_checking(object):
	def __init__(self,lemmatized,bag,term_frequency,inverse_document_frequency,combined):
		self.lemmatized = lemmatized
		self.bag = bag
		self.term_frequency = term_frequency
		self.inverse_document_frequency = inverse_document_frequency
		self.combined = combined

	#define bag of words function
	def bag_of_words(self):
		words_used = {}
		for i in text.lemmatized:
			if i in topic_words:
				if i in words_used.keys():
					words_used[i] += 1
				else:
					words_used[i] = 1
		self.bag = words_used

	#define TF-IDF function
	def TF_IDF(self,word):
		total_words = len(text.lemmatized)
		self.term_frequency = total_words / self.bag[word]

		return(None,None)

	#define cosine similarity function
	def cosine_similarity(self):
		pass


#create class for spell checking
class spell_checking(object):
	def __init__(self,checking):
		self.checking = checking
	
	#define functions to try edits on current checking word
	def deletes(self,iteration,secondary_edit,word):
		known = []
		everything = []
		#check if the process is a primary edit
		if iteration == 1:
			editing = list(word)
			#remove one letter at a time and see if it creates an existent word
			for i in range(0,len(editing)):
				editing = list(word)
				editing.pop(i)
				edited = "".join(editing)
				if edited.lower() in words.words():
					known.append(edited)
				#next line removed because everything is no longer needed as there are no secondary edits
				#everything.append(edited)
			return(known,everything)
		##SECONDARY EDITS CODE REMOVED DUE TO VERY LARGE RUN TIME
		"""
		#check if the process is a secondary edit
		elif iteration == 2:
			editing = list(secondary_edit)
			#remove one letter at a time and see if it creates an existent word
			for i in editing:
				editing = list(secondary_edit)
				editing.remove(i)
				edited = "".join(editing)
				if edited.lower() in words.words():
					known.append(edited)
			return(known)
		"""

	def transposes(self,iteration,secondary_edit,word):
		known = []
		everything = []
		#check if the process is a primary edit
		if iteration == 1:
			editing = list(word)
			#switch the places of consequetive and check if existent words are created
			for i in range(0,len(editing)-1):
				editing = list(word)
				holding = editing[i+1]
				editing[i+1] = editing[i]
				editing[i] = holding
				edited = "".join(editing)
				if edited.lower() in words.words():
					known.append(edited)
				#next line removed because everything is no longer needed as there are no secondary edits
				#everything.append(edited)
			return(known,everything)
		##SECONDARY EDITS CODE REMOVED DUE TO VERY LARGE RUN TIME
		"""
		#check if the process is a secondary edit
		elif iteration == 2:
			editing = list(secondary_edit)
			#switch the places of consequetive and check if existent words are created
			for i in range(0,len(editing)-1):
				editing = list(secondary_edit)
				holding = editing[i+1]
				editing[i+1] = editing[i]
				editing[i] = holding
				edited = "".join(editing)
				if edited.lower() in words.words():
					known.append(edited)
			return(known)
		"""


	def replaces(self,iteration,secondary_edit,word):
		known = []
		everything = []
		#check if the process is a primary edit
		if iteration == 1:
			editing = list(word)
			#try switching letters with each letter of the alphabet
			for i in range(0,len(editing)):
				alphabet = list(string.ascii_lowercase)
				for j in alphabet:
					editing = list(word)
					editing[i] = j
					edited = "".join(editing)
					if edited.lower() in words.words():
						known.append(edited)
					#next line removed because everything is no longer needed as there are no secondary edits
					#everything.append(edited)
			return(known,everything)
		##SECONDARY EDITS CODE REMOVED DUE TO VERY LARGE RUN TIME
		"""
		#check if the process is a secondary edit
		elif iteration == 2:
			editing = list(secondary_edit)
			#try switching letters with each letter of the alphabet
			for i in range(0,len(editing)):
				alphabet = list(string.ascii_lowercase)
				for j in alphabet:
					editing = list(secondary_edit)
					editing[i] = j
					edited = "".join(editing)
					if edited.lower() in words.words():
						known.append(edited)
			return(known)
		"""

	def inserts(self,iteration,secondary_edit,word):
		known = []
		everything = []
		#check if the process is a primary edit
		if iteration == 1:
			editing = list(word)
			#creates an empty index at the end to attempt inserts at end of the word
			editing.append("")
			#try switching letters with each letter of the alphabet
			for i in range(0,len(editing)):
				alphabet = list(string.ascii_lowercase)
				for j in alphabet:
					editing = list(word)
					editing.append("")
					editing.insert(i,j)
					edited = "".join(editing)
					edited = edited.strip()
					if edited.lower() in words.words():
						known.append(edited)
					#next line removed because everything is no longer needed as there are no secondary edits
					#everything.append(edited)
			return(known,everything)
		##SECONDARY EDITS CODE REMOVED DUE TO VERY LARGE RUN TIME
		"""
		#check if the process is a secondary edit
		elif iteration == 2:
			splitted = list(secondary_edit)
			#try switching letters with each letter of the alphabet
			for i in range(0,len(splitted)):
				alphabet = list(string.ascii_lowercase)
				for j in alphabet:
					editing = list(secondary_edit)
					editing.insert(i,j)
					edited = "".join(editing)
					if edited.lower() in words.words():
						known.append(edited)
			return(known)
		"""

	def spelling_probs(self,possibles):
		#read the big text probabilities document
		big_text = open('C:\\Users\\User\\Desktop\\NEA\\data\\sherlock_probs.txt', 'r').read()
		frequencies = eval(big_text)
		relevant_frequencies = {}
		missing = []
		keys = frequencies.keys()
		#Find frequencies of relevant words for comparisons
		for i in possibles:
			if i in keys:
				relevant_frequencies[i] = frequencies.get(i)
			else:
				missing.append(i)
		#Compare relevant frequencies to find the greatest (most likely word)
		greatest = [None,0]
		for i in relevant_frequencies.keys():
			if relevant_frequencies[i] > greatest[1]:
				greatest[0] = i
				greatest[1] = relevant_frequencies[i]
		return(greatest)





#define main function for whole program
def main():
	initial = preprocessing(input("User Input Text Goes Here!!!:  "))
	raw_text = initial.user
	tokenized = initial.tokenizer(initial.user)
	lemmatized = initial.lemmatizer(initial.user)
	text = processing(raw_text,tokenized,lemmatized,10)
	text.main(text.raw_text,text.tokenized,text.lemmatized)
	

main()





