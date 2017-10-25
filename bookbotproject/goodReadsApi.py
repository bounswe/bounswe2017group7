from goodreads import client

goodreads_key = "UfEAj6yQFcghrsqrZpQ"
goodreads_secret = "AgAug5etGSAYceT2SeLGBZLMm803I6LiQSxSnGubOjg"
gc = client.GoodreadsClient(goodreads_key,goodreads_secret)


"""TODO : add bunch of methods like ,search(response): takes response as parameter coming from wit.ai intent and searches .... """

#Prints 20 of different title of book related to keyword

def search_by_author(intent):
	str = "author"
	book = gc.search_books(intent,str)
	return search_books
def search_by_genre(intent):
	str = "genre"
	book = gc.search_books(intent,str)
	return book
def search_by_title(intent):
	str = "title"
	book = gc.search_books(intent,str)
	return book


