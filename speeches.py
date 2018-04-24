# Extracts all speeches from 习近平重要讲话数据库
# Writes them into a single file named for the date/time

import sys
import urllib.request
from bs4 import BeautifulSoup
import datetime

# homepage of the website
INDEX = 'http://jhsjk.people.cn/'

START = '<s>'
END = '</s>'

# speeches are organized in a class
class Speech:

	count = 0
	all = []
	ids = {}

	def __init__(self, id, title, date, category):
		self.id = id
		self.title = title
		self.date = date
		self.cats = [category]
		self.text = ''
		self.__class__.count += 1
		self.__class__.all.append(self)
		self.__class__.ids[id] = self

	def __str__(self):
		return "{} {} {} {}".format(
			self.id, self.date, self.cats, self.title)

	def has_id(id):
		if id in Speech.ids:
			return Speech.ids[id]
		return False

	def add_cat(self, category):
		self.cats.append(category)

	def add_text(self, text):
		self.text = text

	def print_speech(self, n):
		info = '\n{}*{}*{}*{}*{}\n'.format(
			n, self.date, self.title, self.cats, self.id)
		result = START + info + self.text + '\n' + END + '\n'
		return result

	def sort_speeches():
		Speech.all = sorted(
			Speech.all, key=lambda speech: speech.date)


# makes the name of the output file
# based on the current date and time
def make_filename():
	now = datetime.datetime.now()
	time = [now.year, now.month, now.day, now.hour, now.minute]
	for i, n in enumerate(time):
		s = str(n)
		if len(s) < 2:
			time[i] = '0' + s
	second = '{}{}{}_{}{}'.format(
		time[0], time[1], time[2], time[3], time[4])
	first = 'xi_'
	third = '.txt'
	result = first + second + third
	return result


# given the first page url and name of a category
# make speech objects for all of the articles in the category
# recursively finds all of the pages in the category
def oneCategory(url, category):
	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page, 'html.parser')

	# find and create speech objects
	box = soup.find('div', class_='fr')
	links = box.find('ul')('li')
	for link in links:

		# get the id, title, and date
		id = link.find('a').get('href').split('/')[1]
		s = Speech.has_id(id)

		# speech exists in a previous category
		if s:
			s.add_cat(category)

		# new speech
		else:
			title, has_date = link.get_text().split('[')
			date = int(has_date.strip()[:-1].replace('-', ''))
			s = Speech(id, title, date, category)

			# follow the speech link and add text of speech
			speech_url = INDEX + 'article/' + id
			speech_page = urllib.request.urlopen(speech_url)
			speech_soup = BeautifulSoup(speech_page, 'html.parser')
			text = speech_soup.find('div', class_='d2txt_con').get_text()
			s.add_text(text)

	# recursively call function on next page of articles
	pagination = box.find('div', class_='pagination')
	if pagination == None:
		return
	numbers = pagination.find('ul')('li')
	item = str(numbers[0])
	count = 1
	while 'active' not in item and count < len(numbers):
		item = str(numbers[count])
		count += 1
	if count >= len(numbers):
		return
	else:
		next = numbers[count]
		nextLink = next.find('a').get('href')
		oneCategory(nextLink, category)


# identifies all of the categories and their starting links
# calls oneCategory to get the info on the speeches
def categories():
	page = urllib.request.urlopen(INDEX).read()
	soup = BeautifulSoup(page, 'html.parser')
	box = soup.find('div', class_='w1014')
	links = box('a')
	for link in links:
		url = INDEX + str(link.get('href'))
		category = str(link.find('img').get('title'))
		print('Currently finding ' + category + 'category')
		oneCategory(url, category)


# writes speeches to file
# filename taken by user input
def writeSpeeches(filename):
	f = open(filename, 'w')

	# write number of speeches file
	print('Writing to {}'.format(filename))
	total = 'Total Speeches:' + str(Speech.count) + '\n\n'
	f.write(total)

	# write speeches to file
	for i, s in enumerate(Speech.all):
		f.write(s.print_speech(i))

	f.close


def main():

	filename = make_filename()
	categories()
	Speech.sort_speeches()
	writeSpeeches(filename)


main()
