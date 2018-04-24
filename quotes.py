import re
import collections
from collections import defaultdict
import operator
from classes import Work, Verse
from classes import Quoting, Speech, Paragraph, Edict
from classes import GRAM

'''GRAM = int(input('Length of n-gram: '))

while GRAM < 1:
	print('Please pick a positive integer for the n-gram length.')
	GRAM = int(input('Length of n-gram: '))'''

LUNYU_FILE = 'lunyu_simp.txt'
LAOZI_FILE = 'laozi_simp.txt'
XI_FILE = 'xi_20180420_2149.txt'
HAN_FILE = 'han_simp.html'
TANG_FILE = 'tang_simp.htm'
SONG_FILE = 'song_simp.txt'


def clear_punct(l):
	result = re.sub('[！,，、﹑？「」：。『』；“”☆●□]', '', l)
	return result


def lunyu_preprocess(line):
	l = line.strip()

	if '（' not in line:
		return (None, None)
	
	# get verse number from inside parens at end of line
	l = l[::-1]
	right, left = l.split('（', 1)
	right = right[::-1]
	left = left[::-1]
	orig_number = right.split('）')[0]
	ones, decimal = orig_number.split('.')
	if len(decimal) < 2:
		decimal = '0' + decimal
	ones = int(ones) * 100
	decimal = int(decimal)
	number = ones + decimal

	# get text stripped of punctuation
	text = left.split('.')[1].strip()
	text = re.sub('[！,，、﹑？「」：。『』；()]', '', text)
	#print('{} {}'.format(number, text))
	return (number, text)


def laozi_preprocess(line):
	if '.' not in line:
		return (None, None)

	l = line.strip()
	number, text = l.split('.')
	number = int(number)
	text = re.sub('[！,，、﹑？「」：。『』；]', '', text)
	return (number, text)


def get_grams(w, pre):
	f = open(w.file)
	for line in f:
		number, text = pre(line)
		if number:
			v = Verse(number, text)
			w.add_verse(v)
			for i in range(len(text) - (GRAM - 1)):
				g = text[i:i + GRAM]
				if v.number not in w.grams[g]:
					w.grams[g].append(v)

			# count chars
			for n in text:
				w.c_counts[n] += 1
	f.close

# want to add all the info to the speech
# i guess i can make objects for speeches without quotes
# add verses to quotes
def xi_process(X, w):

	f = open(XI_FILE)
	s = None

	# states
	BLANK = 0
	INFO = 1
	SPEECH = 2

	# start state
	state = BLANK

	for line in f:
		l = line.strip()

		# BLANK: keep going, switch to info
		if state == BLANK:
			if l[:3] == '<s>':
				state = INFO

		# INFO: get link, switch to article
		elif state == INFO:
			date, title, category, id = l.split('*')[1:]
			date = int(date)
			id = int(id)
			s = Speech(date, id, category, title, X)
			state = SPEECH

		# SPEECH: check for gram
		elif state == SPEECH:

			# done with speech
			if l[:4] == '</s>':
				X.check_speech(s)
				s = None
				state = BLANK

			# blank line
			elif len(l) == 0:
				pass

			# make a new Paragraph
			else:
				p = s.add_paragraph(l)

				# check each n-gram in quoting paragraph
				sentence = re.sub('[！,，、﹑？「」：。『』；“ ”]', '', l)
				for i in range(len(sentence) - (GRAM - 1)):
					g = sentence[i:i + GRAM]

					# found a quote!
					if g in w.grams:
						p.add_quote(w, g, i)

				s.check_paragraph(p)
	f.close


def edict_process(Q, w):

	f = open(Q.file)

	count = 0
	for line in f:
		#if count > 200:
			#exit()

		l = line.strip()
		e = Edict(count, l, Q, w)
		sentence = clear_punct(l)

		for i in range(len(sentence) - (GRAM - 1)):
			g = sentence[i:i + GRAM]

			# found a quote!
			if g in w.grams:
				e.add_quote(g)

		count += 1

def main():

	Lunyu = Work('Lunyu', LUNYU_FILE)
	get_grams(Lunyu, lunyu_preprocess)

	Xi = Quoting('Xi', XI_FILE, Lunyu)
	xi_process(Xi, Lunyu)

	Han = Quoting('Han', HAN_FILE, Lunyu)
	edict_process(Han, Lunyu)

	Tang = Quoting('Tang', TANG_FILE, Lunyu)
	edict_process(Tang, Lunyu)

	Song = Quoting('Song', SONG_FILE, Lunyu)
	edict_process(Song, Lunyu)

	#print(Lunyu.print_chart())
	print(len(Lunyu.verses))

main()



