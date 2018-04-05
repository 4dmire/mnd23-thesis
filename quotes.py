import re
import collections
from collections import defaultdict



GRAM = 5
LUNYU_FILE = 'lunyu_simp.txt'
LAOZI_FILE = 'laozi_simp.txt'
XI_FILE = 'xi_mar_26.txt'
HAN_FILE = 'han_simp.html'
TANG_FILE = 'tang_simp.htm'


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


class Verse:

	def __init__(self, number, text):
		self.number = number
		self.text = text
		self.work = None
		self.index = 0
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

	def add_quote(self, source, id, desc):
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


def lunyu_preprocess(line):
	l = line.strip()

	if '（' not in line:
		return (None, None)
	
	# get verse number from inside parens at end of line
	l = l[::-1]
	right, left = l.split('（', 1)
	right = right[::-1]
	left = left[::-1]
	number = float(right.split('）')[0])

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
				'''if len(grams[g]) > 1:
					print(g)
					print(grams[g])'''
	f.close


def xi_process(w):
	f = open(XI_FILE)
	category = ''
	link = ''

	# states
	BLANK = 0
	INFO = 1
	ARTICLE = 2

	# start state
	state = BLANK

	for line in f:
		l = line.strip()

		# BLANK: keep going, get cat, switch to info
		if state == BLANK:
			if l[:3] == 'CAT':
				category = l.split(':')[1]
				#print(category)
			if l[:3] == '<s>':
				state = INFO

		# INFO: get link, switch to article
		elif state == INFO:
			full = l.split('*')[1]
			link = full.split('/')[-1]
			state = ARTICLE

		# ARTICLE: check for gram
		elif state == ARTICLE:
			hi = 4
			if l[:4] == '</s>':
				state = BLANK
			else:
				sentence = re.sub('[！,，、﹑？「」：。『』；“ ”]', '', l)
				for i in range(len(sentence) - (GRAM - 1)):
					g = sentence[i:i + GRAM]

					# found a quote!
					if g in w.grams:
						for index in w.grams[g]:
							v = w.verses[index]
							# only want each verse/link pair once
							if link not in v.xi:
								v.add_quote('xi', link, [category, g])
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
					for index in w.grams[g]:
						v = w.verses[index]
						# only want each verse/edict pair once
						if (file == HAN_FILE and title not in v.han) or (
							file == TANG_FILE and title not in v.tang):
							v.add_quote(str(file), title, [emperor, g])
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
	print(result[:-2])


Lunyu = Work('Lunyu', LUNYU_FILE)
get_grams(Lunyu, lunyu_preprocess)

xi_process(Lunyu)
edict_process(Lunyu, HAN_FILE)
edict_process(Lunyu, TANG_FILE)
print_results(Lunyu, [True, True, True])


'''Laozi = Work('Laozi', LAOZI_FILE)
get_grams(Laozi, laozi_preprocess)

xi_process(Laozi)
edict_process(Laozi, HAN_FILE)
edict_process(Laozi, TANG_FILE)
print_results(Laozi, [True, False, False])'''

