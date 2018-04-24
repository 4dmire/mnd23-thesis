from collections import defaultdict

GRAM = 4
LOOKING = 1320
		# 102, 1124, 1205, 1601

'''GRAM = int(input('Length of n-gram: '))

while GRAM < 1:
	print('Please pick a positive integer for the n-gram length.')
	GRAM = int(input('Length of n-gram: '))'''

# one of the quoted texts
class Work:

	def __init__(self, name, file):
		self.name = name
		self.file = file
		self.verses = []
		self.c_counts = defaultdict(int)
		self.grams = defaultdict(list)

	def add_verse(self, v):
		v.work = self
		v.index = len(self.verses)
		self.verses.append(v)

	def print_verses(self):
		result = 'Verses from {}\n\n'.format(self.name)
		for v in self.verses:
			if v.quoted():
				result += v.print_all() + '\n'
		return result

	def print_chart(self):
		result = 'Verses from {} with {}-gram\n\n'.format(
			self.name, GRAM)
		result += 'V\tX\tH\tT\tS\n\n'
		for v in self.verses:
			if v.quoted():
				result += v.chart_row() + '\n'
		return result


# an individual verse
class Verse:

	def __init__(self, number, text):
		self.number = number
		self.text = text
		self.work = None
		self.quoting = {}

	def __repr__(self):
		return '"verse({}, {}, {})"'.format(
			repr(self.number), repr(self.index), repr(self.text))

	def __str__(self):
		return "Verse {} (index {}): {}".format(
			self.number, self.index, self.text)


	def quoted(self):
		result = False
		for q_text, value in self.quoting.items():
			if value[0] > 0:
				result = True
		return result

	def print_all(self):
		result = ''
		for q_text, value in self.quoting.items():
			if value[0] > 0:
				result = str(self) + '\n'
				result += '{}\t{}: '.format(
					q_text.name, value[0])
				for inst, gram in value[1].items():
					s_inst = str(inst)
					length = len(s_inst)
					if length == 8:
						result += s_inst + ' '
					if gram:
						result += str(gram)
						result += ', '
				if result[-2:] == ', ':
					result = result[:-2]
				result += '\n'
		return result

	def chart_row(self):
		row = str(self.number)
		sum = 0
		for i, Q in enumerate(Quoting.all):
			row += '\t'
			n = self.quoting[Q][0]
			if n > 0:
				row += str(n)
				sum += n
		row += '\t' + str(sum)
		return row

	def add_quoting(self, quoting_text):
		self.quoting[quoting_text] = [0, defaultdict(list)]


# one of the quoting texts
class Quoting:

	all = []

	def __init__(self, name, file, w):
		self.name = name
		self.file = file
		self.q_speeches = []
		self.q_count = 0
		self.v_dict = defaultdict(int)	# might take this out later
		self.char_counts = defaultdict(int)
		for v in w.verses:
			v.add_quoting(self)
		self.all.append(self)

	def __repr__(self):
		return '"{} quoting"'.format(self.name)

	def __str__(self):
		return '{} from file {}'.format(self.name, self.file)

	def print_by_speech(self):
		result = 'In {}, {} total quotes in {} speeches\n\n'.format(
			self.name, self.q_count, len(self.q_speeches))

		for i, s in enumerate(self.q_speeches):
			result += '\n#' + str(i + 1) + '\n'
			result += s.print_quotes() + '\n'
		return result

	def print_by_edict(self):
		result = 'In {}, {} total quotes in {} edicts\n\n'.format(
			self.name, self.q_count, len(self.q_speeches))
		for e in self.q_speeches:
			result += '\n' + e.print_quotes()
		return result

	# only keep speeches that have quotes
	def check_speech(self, s):
		if s.q_paragraphs:
			self.q_speeches.append(s)
			return True
		return False

	def check_edict(self, e):
		#if 
		if e.quotes:
			self.q_speeches.append(e)
			return True
		return False


# one of Xi's speeches
class Speech:

	n = 0
	
	def __init__(self, date, id, category, title, parent):
		self.date = date
		self.id = id
		self.category = category
		self.title = title
		self.parent = parent
		self.p_count = 0
		self.q_paragraphs = []

	def __str__(self):
		return 'date: {}\t id: {}\ttitle: {}'.format(
			self.date, self.id, self.title)

	def print_quotes(self):
		result = '{}\t{}\n\t{}\t{}\t{}\n\n'.format(
			self.date, self.title, self.id, self.p_count, self.category)
		for p in self.q_paragraphs:
			result += p.print_quotes() + '\n'
		result = result[:-1]
		return result

	def add_paragraph(self, text):
		self.p_count += 1
		p = Paragraph(self, text, self.p_count)
		return p

	# only keep paragraphs that have quotes
	def check_paragraph(self, p):
		if p.quotes:
			self.q_paragraphs.append(p)
			return True
		return False


# a single line within a speech
class Paragraph:

	def __init__(self, speech, context, number):
		self.parent = speech
		self.grandp = self.parent.parent
		self.context = context
		self.number = number

		# [[verse objects], quote]
		self.quotes = []

	def __str__(self):
		result = 'para {} in speech {}\n{}'.format(
			self.number, self.parent.id, self.context)

	def print_quotes(self):
		result = '{}\t\t\t{}\n'.format(
			self.number, self.context)
		for q in self.quotes:
			v_nums = ''
			for v in q[0]:
				v_nums += (str(v.number)) + (', ')
			v_nums = v_nums[:-2]
			result += '\t\t{}\t{}\n'.format(
				v_nums, q[1])
		return result

	def add_quote(self, w, g, i):
		vs = w.grams[g]


		for v in vs:
			if v.number == LOOKING:
				print(v.number)
				print(self.parent)
				print(g)
				print('---')

		# no quotes yet? add this one
		if not self.quotes:
			self.add_it(w, g, i, vs)
			return True

		# different quote so add
		last = self.quotes[-1][1][-(GRAM - 1):]
		if last != g[:GRAM - 1]:
			self.add_it(w, g, i, vs)
			return True

		# otherwise extend
		else:
			self.quotes[-1][0] = vs
			self.quotes[-1][1] += g[-1]
			self.grandp.char_counts[g[-1]] += 1

			# extend quote in verse
			for v in vs:
				v_xi = v.quoting[self.grandp]
				if not v_xi[1][self.parent]:
					pass
				else:
					v_xi[1][self.parent.id][1] += g[-1]
			return False


	def add_it(self, w, g, i, vs):
		v_row = [self.number, g]
		self.quotes.append([vs, g])
		for c in g:
			self.grandp.char_counts[c] += 1

		# add it to verse
		for v in vs:
			self.grandp.q_count += 1
			self.grandp.v_dict[v] += 1
			v_xi = v.quoting[self.grandp]
			v_xi[0] += 1
			v_xi[1][self.parent.id] = v_row

		# add stars to context
		j = i
		old = self.context
		while old[j + 1] != g[1] and j < len(old):
			j += 1
		self.context = old[:j] + '**QUOTE' + old[j:]


class Edict:

	def __init__(self, count, text, parent, work):
		self.id = count
		self.text = text
		self.parent = parent
		self.work = work
		self.quotes = []

	def __str__(self):
		result = self.text
		return result

	def print_quotes(self):
		result = '\n\n' + str(self.id) + self.text + '\n'

	def add_quote(self, g):
		vs = self.work.grams[g]
		
		for v in vs:
			if v.number == LOOKING:
				print(v.number)
				print(self.parent)
				print(g)
				print('---')

		p = False
		'''for v in vs:
			if v.number == 1919:
				print(g)
				p = True'''

		# no quotes yet? add this one
		if not self.quotes:
			self.add_it(g, vs)
			return True

		# different quote so add
		last = self.quotes[-1][1][-(GRAM - 1):]
		if last != g[:GRAM - 1]:
			self.add_it(g, vs)
			return True

		# otherwise extend
		# PROBLEM: NOT SAVING ALL THE QUOTES, DELETING SOME
		else:
			'''if p:
				print(g)
				print(vs)
				print(self.quotes[-1][1])'''
			self.quotes[-1][0] = vs
			self.quotes[-1][1] += g[-1]
			'''if p:
				print(self.quotes[-1][1])'''
			self.parent.char_counts[g[-1]] += 1

			# extend in verse
			for v in vs:
				v_parent = v.quoting[self.parent]
				if not v_parent[1][self.parent]:
					pass
				else:
					#if v.number == 1919:
						#print(g)
					v_xi[1][self.parent][1] += g[-1]
			return False

	def add_it(self, g, vs):
		v_row = [self.id, g]
		self.quotes.append([vs, g])
		for c in g:
			self.parent.char_counts[c] += 1

		# add it to verse
		for v in vs:
			self.parent.q_count += 1
			v_parent = v.quoting[self.parent]
			v_parent[0] += 1
			v_parent[1][self.id].append(g)
			#if v.number == 1919:
				#print(v_row)
				#print(v.quoting[self.parent])

		# add stars to context
		i = 0
		old = self.text
		while old[i + 1] != g[1] and i < len(old):
			i += 1
		self.text = old[:i] + '**QUOTE' + old[i:]

