import requests
import xmltodict
import json


goodreads_key = "UfEAj6yQFcghrsqrZpQ"
goodreads_secret = "AgAug5etGSAYceT2SeLGBZLMm803I6LiQSxSnGubOjg"
url = "https://www.goodreads.com/search.xml?key=" + goodreads_key + "&q="

def search_helper(url):
	response = requests.get(url)
	converted_response = xmltodict.parse(response.content)
	print("Query time : "+ converted_response['GoodreadsResponse']['search']['query-time-seconds'])
	works = converted_response['GoodreadsResponse']['search']['results']['work']
	return works

def search_by_author(author):
	global url
	url += author + "&search[field]=author"
	return search_helper(url)

def search_by_genre(genre):
	global url
	url += genre + "&search[field]=genre"
	return search_helper(url)

def search_by_name(title):
	global url
	url += title + "&search[field]=title"
	return search_helper(url)

