first = list(input("What is your first word?"))
second = list(input("What is your second word?"))
shared = []
for i in range(0,len(first)):
	if first[i] in second:
		print(first[i] + " found in second word")
		shared.append(first[i])
		for j in range(0,len(second)):
			if second[j] == first[i]:
				second[j] = "" 
				break
if len(shared) == len(first):
	print("First word can be made using letters from the second word")
else:
	print("First word cannot be made using letters from the second word")

