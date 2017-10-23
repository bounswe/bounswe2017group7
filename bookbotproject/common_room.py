from goodreads import client
import telegrambot

goodreads_key = "UfEAj6yQFcghrsqrZpQ"
goodreads_secret = "AgAug5etGSAYceT2SeLGBZLMm803I6LiQSxSnGubOjg"
gc = client.GoodreadsClient(goodreads_key,goodreads_secret)


""" this is a draft code, telegram api, goodreads api and wit ai can send messages among themselves or can make necessary things, for the sake of simplicity we created this py file"""

"""TODO : add bunch of methods like ,search(response): takes response as parameter coming from wit.ai intent and searches .... """

def main():
	print("this is main")
	response = telegrambot.get_next_message_by_response("aa")
	print(response)
	book = gc.search_books(response)
	for i in book :
		print(i.title)

if __name__ == '__main__':
	main();

