# Extract text of articles from 习近平重要讲话数据库
# Write it into a file with a name taken from user input

import sys
import urllib.request
from collections import OrderedDict
from bs4 import BeautifulSoup

# homepage of the website
index = 'http://jhsjk.people.cn/'

# total number of articles
n = 0

# filename from user input
filename = input('Name of new file: ')

# ordered dictionary of categories of articles
# keys are category names; values are article url lists
# ex: 经济, ['article/29780020', ...]
data = OrderedDict()


# populates n and data
# by identifying the categories calling oneCategory
def categories():
	page = urllib.request.urlopen(index).read()
	soup = BeautifulSoup(page, 'html.parser')
	box = soup.find('div', class_='w1014')
	links = box('a')
	global n
	global data
	for link in links:
		url = index + str(link.get('href'))
		name = str(link.find('img').get('title'))
		data[name] = []
		print('Currently finding ' + name + 'category')
		oneCategory(url, data[name])
		n += len(data[name])


# given the url of the first page and a list of articles
# adds article urls in that category to articles
def oneCategory(url, articles):
	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page, 'html.parser')

	# find and add article links
	box = soup.find('div', class_='fr')
	links = box.find('ul')('li')
	for link in links:
		articles.append(str(link.find('a').get('href')))

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
		oneCategory(nextLink, articles)


# writes the contents of n and data to a file
# filename taken by user input
def writeArticles():
	global filename
	f = open(filename, 'w')

	# write number of articles
	pages = 'Total Articles: ' + str(n)
	f.write(pages)
	f.write('')

	# write articles
	count = 1
	for key, value in data.items():
		print('Currently writing ' + key + 'category')
		f.write(key)
		for article in value:
			url = index + article
			info = oneArticle(url)
			f.write(str(count) + ': ' + url)
			f.write(info[0])
			f.write(info[1])
			count += 1
	f.close


# given an article url and filename, 
# return a list of the article title + speech contents
def oneArticle(url):
	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page, 'html.parser')

	# find title and content of speech
	title = soup.find('h1').get_text()
	speech = soup.find('div', class_='d2txt_con').get_text()
	return[title, speech]


# call the functions
categories()
writeArticles()


