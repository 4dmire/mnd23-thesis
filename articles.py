import sys
import urllib.request
from collections import OrderedDict
from bs4 import BeautifulSoup

# Extract text of articles from 习近平重要讲话数据库
# Write it into a file with a name taken from user input

index = "http://jhsjk.people.cn/"


# fix this!! so close <3
def writeArticles(data, n):
	pages = 'Total Articles: ' + str(n)
	filename = input("Type name of new file: ")
	f = open(filename, 'w')
	f.write(pages)
	f.write('# of total articles')
	for category in data:
		f.write(category.key)
		for article in category.value:
			url = index + str(article)
			info = oneArticle(url)
			f.write(info[0])
			f.write(info[1])
	f.close

# given an article url and filename, 
# write the article (title and contents) to the file
def oneArticle(url):
	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page, 'html.parser')
	# find title and content of speech
	title = soup.find('h1').get_text()
	speech = soup.find('div', class_='d2txt_con').get_text()
	# write to file
	return[title, speech]

def onePage():
	'hi'

# target = input("Name of file to write to: ")

# http://jhsjk.people.cn/result?type=101

# given the url of the first page
# prints out all the article urls for all in that category
def oneCategory(url, articles):
	print('')
	print('----page----')
	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page, 'html.parser')
	box = soup.find('div', class_='fr')
	links = box.find('ul')('li')
	for link in links:
		articles.append(link.find('a').get('href'))
	print(url)
	pagination = box.find('div', class_='pagination')
	if pagination == None:
		return
	numbers = pagination.find('ul')('li')
	print(numbers)
	item = str(numbers[0])
	count = 1
	while 'active' not in item and count < len(numbers):
		item = str(numbers[count])
		count += 1
	if count >= len(numbers):
		return
	else:
		next = numbers[count]
		print(next)
		nextLink = next.find('a').get('href')
		oneCategory(nextLink, articles)

def categories():
	page = urllib.request.urlopen(index).read()
	soup = BeautifulSoup(page, 'html.parser')
	box = soup.find('div', class_='w1014')
	links = box('a')
	n = 0						# number of total articles
	data = OrderedDict()
	for link in links:
		url = index + str(link.get('href'))
		print(url)
		name = (link.find('img').get('title'))
		data[name] = []
		oneCategory(url, data[name])
		n += len(data[name])
	writeArticles(data, n)

# jingji_pages = int(input("Number of 经济 pages: "))
# zhengzhi_pages = int(input("Number of 经济 pages: "))
# jingji_pages = int(input("Number of 经济 pages: "))
# jingji_pages = int(input("Number of 经济 pages: "))
# jingji_pages = int(input("Number of 经济 pages: "))
# jingji_pages = int(input("Number of 经济 pages: "))
# jingji_pages = int(input("Number of 经济 pages: "))

# http://jhsjk.people.cn/article/27847383

# aurl = 'http://jhsjk.people.cn/article/27847383'
# afile = input("prompt: ")

categories()

# writeArticle(afile, aurl)
# oneCategory('http://jhsjk.people.cn/result/3?type=108')

# go to the pages after the active one


