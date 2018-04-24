

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

				if g in w.grams:

				# found a quote!
				if g in w.grams:
					for j, number in enumerate(w.grams[g]):
						v = w.verses[number]
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
