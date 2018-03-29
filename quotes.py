import re
import collections
from collections import defaultdict

# go through each book
# extract the 4 grams
# have a big dict of the 4 grams from lunyu
# first lets see if there are collisions?
# get all the 4grams
# go through the other texts and see

# 4: 588 | 210
# 5: 397 | 115
# 6: 302
# 7: 228

GRAM = 6
LUNYU = "lunyu_simp.txt"
XI = "xi_mar_26.txt"

"""
big overview
make dict of 4 grams in lunyu
	maybe ignore the zi yue and everything later
	for now just get verse #, strip punctuation
	state machine?
go through other texts and see where they overlap w it
"""

"""
context = re.sub("！，❤。～《》：（）【】「」？”“；：、".decode("utf8"),"",context)
"""


def lunyu_preprocess(line):
	l = line.strip()
	
	# get verse number from inside parens at end of line
	l = l[::-1]
	right, left = l.split('（', 1)
	right = right[::-1]
	left = left[::-1]
	number, blank = right.split('）')
	number = float(number)

	# get sentence stripped of punctuation
	blank, focus = left.split('.')
	focus = focus.strip()
	sentence = re.sub('[！,，、﹑？「」：。『』；]', '', focus)
	return (number, sentence)

# might be better to do something w regex lol
# have a list of the 4 grams that go with each verse

def lunyu_process():
	d = {}
	#d['孔子'] = []
	f = open(LUNYU)
	for line in f:
		if '（' in line:
			number, sentence = lunyu_preprocess(line)
			for i in range(len(sentence) - (GRAM - 1)):
				four = sentence[i:i + GRAM]
				if four not in d:
					d[four] = []
					d[four].append([])
					d[four].append([])
				d[four][0].append(number)
				#if len(d[four][0]) > 1:
					#print(four)
					#print(d[four])
	f.close
	return d

# actually I want the verse it references--the gram doesn't matter much

BLANK = 0
INFO = 1
ARTICLE = 2

def xi_process(d):
	count = 0
	lun = d
	f = open(XI)
	number = 0
	sentence = ''
	state = ARTICLE
	for line in f:
		l = line.strip()
		#sentence = re.sub('[！,，、﹑？「」：。『』；“”]', '', l)
		#print(sentence)
		if state == BLANK:
			hi = 4
		elif state == INFO:
			'no'
		elif state == ARTICLE:
			verses = {}
			l = line.strip()
			sentence = re.sub('[！,，、﹑？「」：。『』；“ ”]', '', l)
			for i in range(len(sentence) - (GRAM - 1)):
				four = sentence[i:i + GRAM]
				if four in lun:
					for v in lun[four][0]:
						if v not in verses:
							verses[v] = 1
							lun[four][1].append(sentence)
							print(lun[four][0])
							#print(lun[four])
				# want to know: where do you see the verses appear?
				# just use 4s to get at that
				# need to restructure verses/grams a little
	f.close
	print(count)
	return lun

lun = lunyu_process()
with_xi = xi_process(lun)

