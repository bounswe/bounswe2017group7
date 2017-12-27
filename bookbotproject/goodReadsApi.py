import requests
import xmltodict
import json


goodreads_key = "UfEAj6yQFcghrsqrZpQ"
goodreads_secret = "AgAug5etGSAYceT2SeLGBZLMm803I6LiQSxSnGubOjg"
url = "https://www.goodreads.com/search.xml?key=" + goodreads_key + "&q="

def search_by_author(author):
	global url
	books=[]
	url += author + "&search[field]=author"
	response = requests.get(url)
	converted_response = xmltodict.parse(response.content)
	works = converted_response['GoodreadsResponse']['search']['results']['work']
	for work in works:
		book = work['best_book']['title']
		books.append(book.encode('utf-8'))

	return books

def search_by_genre(genre):
	global url
	books=[]
	url += genre + "&search[field]=genre"
	response = requests.get(url)
	converted_response = xmltodict.parse(response.content)
	works = converted_response['GoodreadsResponse']['search']['results']['work']
	for work in works:
		book = work['best_book']['title']
		books.append(book.encode('utf-8'))

	return books

def search_by_title(intent):
	str = "title"
	book = gc.search_books(intent,str)
	return book


