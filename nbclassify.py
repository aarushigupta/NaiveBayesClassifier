import numpy as np
import sys
from nblearn import data_cleanup

def readFile(file_ext):
	data = None
	with open(file_ext) as f:
		data = f.readlines()  
	return data


def split_into_words(data):
	words_in_reviews = ['' for x in range(len(data))]
	for index, review in enumerate(data):
		try:
			words_in_reviews[index] = review.strip().split()
		except:
			print "Exception in split_into_words"
	return words_in_reviews



def readModelParameters():
	uniqueWords = []
	class_probab = []
	words_labels_mat = []
	filename = "nbmodel.txt"

	with open(filename,'r') as f:
		fileContents = f.readlines()

	SEPARATOR = "******######******######******######******######******"
	flag = 0

	for index in range(len(fileContents)):
		line = fileContents[index].strip()
		if line == SEPARATOR:
			flag += 1
			continue

		if flag == 1:
			uniqueWords = line.split("\t")
			# words_labels_mat = [[] for x in range(len(uniqueWords))]


		if flag == 2:
			words_labels_mat.append(map(float,line.split("\t")))

		if flag == 3:
			class_probab = (map(float,line.split("\t")))

	
	return uniqueWords, words_labels_mat, class_probab



def calc_review_class(test_data, words_in_reviews_test, class_probab):
	class_true_fake_pos_neg = [[] for x in range(len(test_data))]
	filename = "nboutput.txt"

	for index, review in enumerate(words_in_reviews_test):
		feature_probab_true = 0.0
		feature_probab_fake = 0.0
		feature_probab_pos = 0.0
		feature_probab_neg = 0.0
		for word in review:
	   
			if word.endswith('ing'):
				word = word[:-3]
			# if word.endswith('ly'):
			# 	word = word[:-2]
			if word.endswith('ed'):
				 word = word[:-2]

			if word in uniqueWords:
				try:
					feature_probab_true += words_labels_mat[uniqueWords.index(word)][0]
					feature_probab_fake += words_labels_mat[uniqueWords.index(word)][1]
					feature_probab_pos += words_labels_mat[uniqueWords.index(word)][2]
					feature_probab_neg += words_labels_mat[uniqueWords.index(word)][3]
				except:
					print "Exception in calc_review_class"

		probab_review_true = feature_probab_true + class_probab[0]
		probab_review_fake = feature_probab_fake + class_probab[1]
		probab_review_pos = feature_probab_pos + class_probab[2]
		probab_review_neg = feature_probab_neg + class_probab[3]

		try:
			class_true_fake_pos_neg[index].append(review[0])
		except:
			class_true_fake_pos_neg[index].append('RandomId')


		if probab_review_true > probab_review_fake:
			class_true_fake_pos_neg[index].append('True')
		else:
			class_true_fake_pos_neg[index].append ('Fake')

		if probab_review_pos > probab_review_neg:
			class_true_fake_pos_neg[index].append('Pos')
		else:
			class_true_fake_pos_neg[index].append('Neg')


	output = ""
	for row_index in class_true_fake_pos_neg:
		output += " ".join(map(str, row_index)) + "\n"

	with open(filename, 'w') as f:
		f.write(output)
		f.close()

	return class_true_fake_pos_neg
	 



if __name__ == '__main__':


	uniqueWords, words_labels_mat, class_probab = readModelParameters()
	test_data = readFile(sys.argv[1])
	test_data = data_cleanup(test_data)

	words_in_reviews_test = split_into_words(test_data)
	
	class_true_fake_pos_neg = calc_review_class(test_data, words_in_reviews_test, class_probab)
