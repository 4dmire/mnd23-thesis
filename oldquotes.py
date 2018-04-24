import re
import collections
from collections import defaultdict
import operator

GRAM = 4

'''GRAM = int(input('Length of n-gram: '))

while GRAM < 1:
	print('Please pick a positive integer for the n-gram length.')
	GRAM = int(input('Length of n-gram: '))'''

LUNYU_FILE = 'lunyu_simp.txt'
LAOZI_FILE = 'laozi_simp.txt'
XI_FILE = 'xi_apr_18.txt'
HAN_FILE = 'han_simp.html'
TANG_FILE = 'tang_simp.htm'


# one of the quoted texts
class Work:

	def __init__(self, name, file):
		self.name = name
		self.file = file
		self.verses = []
		self.grams = defaultdict(list)

	def add_verse(self, v):
		v.work = self
		v.index = len(self.verses)
		self.verses.append(v)

# an individual verse
class Verse:

	def __init__(self, number, text):
		self.number = numberx
		self.text = text
		self.work = None
		self.index = 0
		self.quoting = {}
		self.xi = {}
		self.han = {}
		self.tang = {}
		self.refs = [0, 0, 0, 0]

	def __repr__(self):
		return '"verse({}, {}, {})"'.format(
			repr(self.number), repr(self.index), repr(self.text))

	def __str__(self):
		return "Verse {} (index {})\n{}\nxi: {}\nhan: {}\ntang: {}".format(
			self.number, self.index, self.text, self.xi, self.han, self.tang)

	def add_quoting(self, quoting_text):
		self.quoted[quoting_text] = {}

	def add_quote(self, quoting_text, id, desc):
		self.refs[0] += 1
		if source == 'xi':
			self.xi[id] = desc
			self.refs[1] += 1
		elif source == 'han_simp.html':
			self.han[id] = desc
			self.refs[2] += 1
		elif source == 'tang_simp.htm':
			self.tang[id] = desc
			self.refs[3] += 1

	def str_refs(self):
		r = self.refs
		result = '{}\t{}\t{}\t{}'.format(r[0], r[1], r[2], r[3])
		return result

# one of the quoting texts
class Quoting:

	def __init__(self, name, file):
		self.name = name
		self.file = file
		self.speeches = []
		self.distinct = []
		self.distinct_count = 0
		self.char_counts = {}


# one of Xi's speeches
class Speech:

	n = 0
	
	def __init__(self, date, id, category, title):
		self.date = date
		self.id = id
		self.category = category
		self.title = title
		self.parent = parent
		self.para_count = 0
		self.q_paragraphs = []

	def add_paragraph(self, text):
		self.para_count += 1
		p = Paragraph()

	# only if it has a quote remember it
	def check_paragraph(self, p):
		pass


# a single line within a speech
class Paragraph:

	def __init__(self, speech, context, number):
		self.parent = speech
		self.context = context
		self.number = number
		self.quotes = []

	def add_quote(self, w, g):
		vs = w.grams[g]
		last = self.quotes[-1][1][-(GRAM - 1):]

		# extend quote in paragraph
		if last == g[:GRAM - 1]:
			self.quotes[-1][0] = vs
			self.quotes[-1][1] += g[-1]
			self.parent.parent.char_counts[g[-1]] += 1

		# add quote to paragraph
		else:
			quotes.append([vs, g])
			for c in g:
				self.parent.parent.char_counts[c] += 1
			for v in vs:




def lunyu_preprocess(line):
	l = line.strip()

	if '（' not in line:
		return (None, None)
	
	# get verse number from inside parens at end of line
	l = l[::-1]
	right, left = l.split('（', 1)
	right = right[::-1]
	left = left[::-1]
	number = right.split('）')[0]

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
				if v.index not in w.grams[g]:
					w.grams[g].append(v.index)

			# count chars
			for n in text:
				if n in char_counts:
					char_counts[n][0] += 1
				else:
					char_counts[n] = [1, 0, 0]
	f.close

# want to add all the info to the speech
# i guess i can make objects for speeches without quotes
# add verses to quotes
def xi_process(w):
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
			state = SPEECH
			s = Speech(date, id, category, title, Xi)

		# SPEECH: check for gram
		elif state == SPEECH:
			if l[:4] == '</s>':
				s.paragraphs = para_count
				para_count = 0
				state = BLANK
			else:

				# make a new Paragraph
				p = s.add_paragraph(l)	

				# check each gram and add if quote
				sentence = re.sub('[！,，、﹑？「」：。『』；“ ”]', '', l)
				for i in range(len(sentence) - (GRAM - 1)):
					g = sentence[i:i + GRAM]

					# found a quote!
					if g in w.grams:
						p.add_quote(w, g)

				# get rid of empty Paragraphs
				s.check_paragraph(p)

	f.close


def edict_process(w, file):
	f = open(file)
	count = 0
	emperor = ''
	title = ''

	for line in f:
		l = line.strip()
		if len(l) < 3:
			pass

		# new emperor
		elif l[:4] == '<h2>':
			# could probably remove more from this
			if '☆' in l:
				emperor = l.split('☆')[1]
			else:
				emperor = l.split('>', 1)[1]
			emperor = emperor.split('<')[0].strip()
		
		# new edict
		elif l[:1] == '○':
			title = l.split('○')[1].strip()
			#print(title)

		# not at first edict yet
		elif title == '':
			pass

		# in text of edict, look for gram
		else:
			sentence = re.sub('[！,，、﹑？「」：。『』；“ ”]', '', l)
			for i in range(len(sentence) - (GRAM - 1)):
				g = sentence[i:i + GRAM]

				# found a quote!
				if g in w.grams:
					for j, index in enumerate(w.grams[g]):
						v = w.verses[index]
						# only want each verse/edict pair once
						if (file == HAN_FILE and title not in v.han) or (
							file == TANG_FILE and title not in v.tang):
							v.add_quote(str(file), title, [emperor, g])

							# count chars in quotes
							if j == 0:
								for c in g:
									#print(g)
									# this is messed up
									if c in char_counts:
										char_counts[c][1] += 1
	f.close


def print_results(w, corpora):
	x = h = t = x_t = h_t = t_t = 0
	result = ''
	q = 'Verse\t\tTotal\tXi\tHan\tTang\n'
	for v in w.verses:
		used = False
		times = 0

		# Xi
		if corpora[0] and len(v.xi) > 0:
			used = True
			x += 1
			x_t += len(v.xi)
			times += len(v.xi)

		# Han
		if corpora[1] and len(v.han) > 0:
			used = True
			h += 1
			h_t += len(v.han)
			times += len(v.han)

		# Tang
		if corpora[2] and len(v.tang) > 0:
			used = True
			t += 1
			t_t += len(v.tang)
			times += len(v.tang)

		if used == True:
			result += str(v) + '\n\n'
		q += (str(v.number) + '\t\t' + v.str_refs() + '\n')

	print('Using a {}-gram for the {}:'.format(GRAM, w.name))
	if corpora[0]:
		print('Xi quoted {} verses a total of {} times.'.format(x, x_t))
	if corpora[1]:
		print('Han quoted {} verses a total of {} times.'.format(h, h_t))
	if corpora[2]:
		print('Tang quoted {} verses a total of {} times.'.format(t, t_t))
	print('')
	print(q)	
	print('')
	#print(result[:-2])


def print_xi_by_verse(w):
	for v in w.verses:
		one_v = '{}'.format(v.number)
		for n, desc in v.xi.items():
			one_v += '\t{}\t{}\t{}\n'.format(
				n, desc[0], desc[1])
		if len(one_v) > 10:
			one_v = one_v[:-1]
		print(one_v)


def print_xi_by_speech(w):
	speeches = {}
	for v in w.verses:
		# s is the unique speech number
		for s, desc in v.xi.items():
			if s not in speeches:
				speeches[s] = [desc[0]]
			speeches[s].append((v.number, desc[1]))

	print('\tIn total, {} different speeches use Lunyu quotes.\n'.format(
		len(speeches)))
	count = 1
	for a, verses in speeches.items():
		one_a = '{})\t{}\t'.format(count, a)
		count += 1
		for i, n in enumerate(verses):
			if i == 0:
				one_a += '{}\n\n'.format(n)
			else:
				one_a += '\t  {}\t{}\n'.format(n[0], n[1])
		one_a += '\n'
		print(one_a)

# broken lol
def print_counts(d):
	s = sorted(d.items(), key = operator.itemgetter(1))
	s = s[::-1]
	print('\t论语\t汉唐\t习')
	for n in s:
		str = '{}:\t{}\t{}\t{}'.format(n[0], n[1][0], n[1][1], n[1][2])
		if n[1][0] < n[1][2]:
			str += '\t****'
		print(str)


Lunyu = Work('Lunyu', LUNYU_FILE)
get_grams(Lunyu, lunyu_preprocess)

xi_process(Lunyu)

edict_process(Lunyu, HAN_FILE)

edict_process(Lunyu, TANG_FILE)
print_counts(char_counts)
print_results(Lunyu, [True, True, True])
print_xi_by_speech(Lunyu)

'''Laozi = Work('Laozi', LAOZI_FILE)
get_grams(Laozi, laozi_preprocess)

xi_process(Laozi)
edict_process(Laozi, HAN_FILE)
edict_process(Laozi, TANG_FILE)
print_results(Laozi, [True, True, True])'''



