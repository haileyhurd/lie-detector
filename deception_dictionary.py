from collections import defaultdict

#ORIGINAL DATASET:

dataset = open("7Truth7LiesDataset.txt")
lines_of_data = dataset.readlines()
deception_dictionary = {}
truth_dictionary = {}
lie_dictionary = {}
truth_number = 0
lie_number = 0
for x in range(len(lines_of_data)):
	if "college," in lines_of_data[x]:
		string = lines_of_data[x]
		lines_of_data[x] = string.replace("college,", "college")
	if "Masters," in lines_of_data[x]:
		string = lines_of_data[x]
		lines_of_data[x] = string.replace("Masters,", "masters")
	if "Doctorate," in lines_of_data[x]:
		string = lines_of_data[x]
		lines_of_data[x] = string.replace("Doctorate,", "doctorate")
	if "INDIA," in lines_of_data[x]:
		string = lines_of_data[x]
		lines_of_data[x] = string.replace("INDIA,", "india")

for x in range(len(lines_of_data)):
	deception_dictionary[x] = lines_of_data[x].split(",")
	#key = lines_of_data[x].split(",")
	#deception_dictionary[key[0]] = lines_of_data[x].split(",")
	x = x + 1

#DICTIONARIES FOR DATASET BY CLASS:

for y in range(len(deception_dictionary)):
	if "truth\n" in deception_dictionary[y]:
		truth_dictionary[truth_number] = deception_dictionary[y]
		truth_number += 1
	elif "lie\n" in deception_dictionary[y]:
		lie_dictionary[lie_number] = deception_dictionary[y]
		lie_number += 1

	# ID KEY:
	# 1st part = person # (men and women are indexed seperately)
	# 2nd part = female or male (f/m)
	# 3rd part = truth or lie (t/l)
	# 4th part = statement number each person did (truths and lies are indexed seperately)
	# Example: 36_f_l_5 is female person number 36's fifth lie

#DICTIONARY OF STATEMENTS FOR EACH CLASS:

truth_statements = []
for x in range(len(truth_dictionary)):
	shortcut = truth_dictionary[x]
	truth_statements += [shortcut[5]]
lie_statements = []
for x in range(len(lie_dictionary)):
	shortcut2 = lie_dictionary[x]
	lie_statements += [shortcut2[5]]
for y in range(len(truth_statements)):
	truth_statements[y] = truth_statements[y].lower()
for y in range(len(lie_statements)):
	lie_statements[y] = lie_statements[y].lower()

#FUNCTION FOR HOW MANY TIMES EACH WORD IS SAID IN TRUTHS/LIES

def word_count(statements):
	word_dictionary = defaultdict(lambda : 1)
	words_in_statement = []
	for number in range(len(statements)):
		words_in_statement = words_in_statement + statements[number].split(" ")
	for x in range(len(words_in_statement)):
		word = words_in_statement[x]
		if not word in word_dictionary:
			word_dictionary[word] = 1
		else:
			word_dictionary[word] = word_dictionary[word] + 1
	return word_dictionary

#DICTIONARIES FOR PROBABILITY

def make_prob_dicts():
	truth_words = word_count(truth_statements)
	lie_words = word_count(lie_statements)

	prior = 0.6
	prob_lie_dict = defaultdict(lambda : 1 - prior)
	prob_truth_dict = defaultdict(lambda : prior)

	for word in lie_words:
		prob_lie_dict[word] = lie_words[word] / float(truth_words[word] + lie_words[word])

	for word in truth_words:
		if prob_lie_dict[word] == 0:
			prob_truth_dict[word] = 1.0
		else:
			prob_truth_dict[word] = truth_words[word] / float(truth_words[word] + lie_words[word])
	return prob_lie_dict, prob_truth_dict

# What is the probability that a sentence is 
lie_dict, truth_dict = make_prob_dicts()

#################################
#PUT SENTENCE HERE WITHIN QUOTES IN LOWERCASE:
test_sentence = "The sky is blue."
#################################

words = test_sentence.split(" ")

prob_lie = 1.0
for word in words:
	prob_lie *= lie_dict[word]


prob_truth = 1.0
for word in words:
	prob_truth *= truth_dict[word]

if prob_truth > prob_lie:
	print "truth"
else:
	print "lie"
