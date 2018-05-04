import numpy as np
import sys

def readFile(file_ext):
	data = None
	with open(file_ext) as f:
		data = f.readlines()  
	return data


def data_cleanup(data):
	symbols_to_remove = [',','.','!','"','@','#','%','^','&','*','(',')','{','}','[',']','|','\\',';',':','<','>','?','/',\
						'`','~','_','+','=',"$"]
	symbols_to_remove += ['0','1','2','3','4','5','6','7','8','9']
	for index,review in enumerate(data):
		try:
			space_index = review.index(" ")
			review_id = review[:space_index + 1]
		except:
			print "Error in finding space_index in data_cleanup"
			continue
		remaining_review = review[space_index :].lower()
		for char in symbols_to_remove:
			remaining_review = remaining_review.replace(char, " ")
		data[index] = review_id + remaining_review

	return data



def split_into_words(data):
	words_in_reviews = ['' for x in range(len(data))]
	for index, review in enumerate(data):
		try:
			words_in_reviews[index] = review.strip().split()
		except:
			print "Exception in split_into_words"
	return words_in_reviews


def remove_stop_words(words_in_reviews):

	stop_words = ['a','about','above','after','again','against','all','am','an','and','any','are','as','at','be',\
				  'because','been','before','being','below','between','both','but','by','could','did','do','does',\
				  'doing','down','during','each','few','for','from','further','had','has','have','having','he',\
				  'd','ll','s','her','here','hers','herself','him','himself','his','how','i','m','ve','if','in',\
				  'into','is','it','its','itself','let','me','more','most','my','myself','nor','of','on','once',\
				  'only','or','other','ought','our','ours','ourselves','out','over','own','same','she','should',\
				  'so','some','such','than','that','the','their','theirs','them','themselves','then','there',\
				  'these','they','re','this','those','through','to','too','under','until','up','very','was',
				  'we','were','what','when','where','which','while','who','whom','why','with','would',\
				  'you','your','yours','yourself','yourselves','l','isn','t','didn','couldn','doesn','haven',\
				  'weren','oughn','re','lets','aren']

	temp_list = []
	for review_index in range(len(words_in_reviews)):
		temp_list = []
		for word in words_in_reviews[review_index]:
			if word not in stop_words:
				temp_list.append(word)
		words_in_reviews[review_index] = temp_list

	return words_in_reviews		


def word_labels(words_in_reviews):


	labels = ['true', 'fake', 'pos', 'neg']
	label_counts = [0 for x in range(len(labels))]
	uniqueWords = []

	words_labels_mat = []
	label_1_index = 0
	label_2_index = 0

	for review in words_in_reviews:
		for index, label in enumerate(labels):
			try:
				if review[1] == label:
					label_1_index = index
					label_counts[label_1_index] += 1
			except:
				print "Exception in review[1] in word_labels"
				label_1_index = index

			try:
				if review[2] == label:
					label_2_index = index
					label_counts[label_2_index] += 1
			except:
				print "Exception in review[1] in word_labels"
				label_2_index = index


		for word in review[3:]:
			if word not in uniqueWords:
				if word.endswith('ing'):
					word = word[:-3]
				# if word.endswith('ly'):
				# 	word = word[:-2]
				if word.endswith('ed'):
					 word = word[:-2]
				uniqueWords.append(word)
				words_labels_mat.append([1 for x in range(len(labels))])
			if word in uniqueWords:
				try:
					words_labels_mat[uniqueWords.index(word)][label_1_index] += 1
					words_labels_mat[uniqueWords.index(word)][label_2_index] += 1
				except:
					print "Exception while inserting values into words_labels_mat"

	words_labels_mat = np.array(words_labels_mat, dtype=np.float64)
	words_labels_mat_sum = np.sum(words_labels_mat, axis = 0)

	count_words = len(uniqueWords)


	for word_index in range(len(words_labels_mat)):
		for class_index in range(len(labels)):
			words_labels_mat[word_index][class_index] = (words_labels_mat[word_index][class_index] * 1.0) / (words_labels_mat_sum[class_index])  

	words_labels_mat = np.log(words_labels_mat)
   
	
	return uniqueWords, label_counts, words_labels_mat
			


def calc_class_probab(data, label_counts):
	count_reviews = len(data)

	probab_true = label_counts[0] * 1.0 / count_reviews
	probab_fake = label_counts[1] * 1.0 / count_reviews
	probab_pos = label_counts[2] * 1.0 / count_reviews
	probab_neg = label_counts[3] * 1.0 / count_reviews

	class_probab = [probab_true, probab_fake, probab_pos, probab_neg]

	return class_probab


def write_model_parameters(uniqueWords, class_probab, words_labels_mat, filename = 'nbmodel.txt'):
	SEPARATOR = "******######******######******######******######******\n"
	output = "******######******######******######******######******\n"

	allWords = ""
	for word in uniqueWords:
		allWords += str(word) + "\t"

	output += allWords + "\n" 
	output += SEPARATOR

	matrixVals = ""
	for words in words_labels_mat:
		matrixVals += '\t'.join(map(str, words)) + '\n'

	output += matrixVals
	output += SEPARATOR

	
	class_probablities = ""
	for probab in class_probab:
		class_probablities += str(probab) + "\t"

	output += class_probablities + "\n" + SEPARATOR


	with open (filename,'w') as f:
		f.write(output)
		f.close()

def write_unique_words(uniqueWords):
	output = ""
	filename = "uniqueWords.txt"
	for word in uniqueWords:
		output += "'" + str(word) + "', "

	with open(filename, 'w') as f:
		f.write(output)
		f.close()

if __name__ == '__main__':


	train_data = readFile(sys.argv[1])
	train_data = data_cleanup(train_data)
	words_in_reviews = split_into_words(train_data)
	words_in_reviews = remove_stop_words(words_in_reviews)

	uniqueWords, label_counts, words_labels_mat = word_labels(words_in_reviews)

	class_probab = calc_class_probab(train_data, label_counts)
	write_model_parameters(uniqueWords, class_probab, words_labels_mat)
	write_unique_words(uniqueWords)