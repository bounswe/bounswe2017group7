import json
import requests
import time
import goodReadsApi
import re
TOKEN = "433004356:AAFzeqBEW8_UgEPDOnJ8bnQAPitaR7gLSSo";
URL = 	"https://api.telegram.org/bot{}/".format(TOKEN);
HOST = "http://127.0.0.1:8000/"

def send_request(url):
	res = requests.get(url);
	content = res.content.decode("utf8");
	return content;


def get_json(url):
	content = send_request(url);
	retrieved_json = json.loads(content);
	return retrieved_json;


def get_updates(offset=None):
	updateURL = URL + "getUpdates?timeout=100"
	if offset:
		updateURL += "&offset={}".format(offset);
	_json = get_json(updateURL);
	return _json;

def check_user(name, user_id, chat_id):
	""" check if user exists"""
	url = HOST + "getUser/{}".format(user_id)
	r = requests.get(url)

	""" if not create new user"""
	if r.status_code == 404:
		try:
			url =  HOST + "addUser/{}/{}/{}/".format(name, user_id, chat_id)
			r = requests.post(url)
			if r.status_code != 200:
				print("Error in check_user")
		except requests.exceptions.RequestException as e:
			print(e) 


def get_last_chat(updates):
	length = len(updates["result"]);
	#print("Get last chatteyim")
	try:
		#print("burasi normal yer")
		name = updates["result"][length-1]["message"]["from"]["first_name"]
		#print("name aldi")
		user_id = updates["result"][length-1]["message"]["from"]["id"];
		#print("userid aldi")
		text = updates["result"][length-1]["message"]["text"];
		#print("text aldi")
		chat_id = updates["result"][length-1]["message"]["chat"]["id"];
		#print("chatid aldi")
		update_id = updates["result"][length-1]["update_id"]; 
		#print("update id aldi")
	except KeyError as e:
		#print("burasi exceptionli")
		name = updates["result"][length-1]["callback_query"]["from"]["first_name"]
		user_id = updates["result"][length-1]["callback_query"]["from"]["id"];
		text = updates["result"][length-1]["callback_query"]["data"];
		chat_id = updates["result"][length-1]["callback_query"]["message"]["chat"]["id"];
		update_id = updates["result"][length-1]["update_id"]; 
		answerCallbackQuery(chat_id)
	#print("name "+name )
	#print(user_id)
	#print chat_id
	check_user(name, user_id, chat_id)

	return [text, chat_id, update_id, user_id];

def get_next_message_by_genre(text, chat_id):
	print("genre " + text)
	
	book = goodReadsApi.search_by_genre(text)
	
	return book


def get_next_message_by_author(text, chat_id):
	print("author " +text)
	
	book = goodReadsApi.search_by_author(text)
	
	return book


def get_next_message_by_title(text, chat_id):
	print("title "+text)
	
	book = goodReadsApi.search_by_name(text)
	
	return book

def answerCallbackQuery(chat_id):
	message = "True"
	sendURL = URL + "answerCallbackQuery?text={}&chat_id={}".format(message, chat_id);	
	sendURL = sendURL.replace("#","No:")
	send_request(sendURL);

def send_message(message, chat_id,reply_markup=""):

	sendURL = URL + "sendMessage?text={}&chat_id={}".format(message, chat_id);
	if reply_markup != "":
		sendURL = sendURL + "&reply_markup={}".format(reply_markup)

	sendURL = sendURL.replace("#","No:")	
	send_request(sendURL);


def send_photo(works, chat_id, begin=0, end=3):
	"""Sends five best books pictures alongside with information """
	newline = "%0A"
	for work in works[begin:end]:

		image_url = work['best_book']['image_url']
		image_url = image_url.encode('utf-8')
		title = work['best_book']['title']
		title = title.encode('utf-8')
		title = title.replace("&","and")

		author = work['best_book']['author']['name']
		author = author.encode('utf-8')
		author = author.replace("&","and")

		try:
			pub_year = work['original_publication_year']['#text']
		except KeyError as e:
			pub_year = "Not Found"
		pub_year = pub_year.encode('utf-8')
		### belki burda utf 8 special char arindirmasi yapabiliriz
		sendURL = URL + "sendPhoto?photo={}&chat_id={}".format(image_url, chat_id)
		sendURL = sendURL + "&caption=" +"Title : " +title +newline+"Author : " +author + newline+"Publication Year : " + pub_year
		sendURL = sendURL.replace("#","No:")
		
		send_request(sendURL);
		time.sleep(0.3);

def main():
	counter = 0
	last_chat = (None, None)
	last_update = None
	end_switch = False
	while True:

		text, chat, update_id, user_id = get_last_chat(get_updates(last_update))

		#Fixer of the bug unicode special char problem
		#print("before text = "+text)
		#text = re.sub('[^A-Za-z0-9]+', ' ', text)
		#print("after text = "+text)
		

		current_Node_r = requests.get(HOST + "getCurrentNode/{}/".format(user_id))		
		json_response = json.loads(current_Node_r.content)
		current_node_intent = json_response['intent']

		#print current_node_intent
		if(text, chat) != last_chat or current_node_intent=="recommendation":
			# Get related response for user message
			r = requests.get(HOST + "getResponse/{}/{}/".format(text, chat))

			print(r.text)

			if end_switch and r.text == '\"Goodbye bookworm!\"':
				end_switch = True
			elif r.text == "\"Get or give information? I can also recommend some books!\"":
				keyboard = '{"inline_keyboard" : [[{"text":"Get information","callback_data":"I want to get information"}],[{"text":"Give information","callback_data":"give info"}],[{"text":"Recommend me some books","callback_data":"recommend"}]]}'
				send_message(r.text,chat,keyboard)

			elif r.text == "\"Do you want to search books? You can also get comments or ratings by saying get comments or get ratings!\"":
				keyboard = '{"inline_keyboard" : [[{"text":"Search by title","callback_data":"search by title"}],[{"text":"Search by author","callback_data":"search by author"}],[{"text":"Search by genre","callback_data":"search by genre"}]]}'
				send_message(r.text,chat,keyboard)
			
			
			elif r.text == "\"Rate a book or comment on a book?\"":
				keyboard = '{"inline_keyboard" : [[{"text":"Rate a book","callback_data":"rate a book"}],[{"text":"Comment on a book","callback_data":"comment on a book"}]]}'
				send_message(r.text,chat,keyboard)

			elif r.text == "\"Do you want more books from this title?\"":
				title=text
				res = get_next_message_by_title(title, chat)
				send_photo(res, chat);
				time.sleep(2)
				keyboard = '{"inline_keyboard" : [[{"text":"Thank you and Goodbye!","callback_data":"goodbye"}],[{"text":"Yesss! Go on!","callback_data":"Yes"}]]}'
				send_message(r.text,chat,keyboard)
				
			elif r.text == "\"Do you want more books from this author?\"":
				author = text
				res = get_next_message_by_author(author, chat)
				send_photo(res, chat);
				time.sleep(2)
				keyboard = '{"inline_keyboard" : [[{"text":"Thank you and Goodbye!","callback_data":"goodbye"}],[{"text":"Yesss! Go on!","callback_data":"Yes"}]]}'
				send_message(r.text,chat,keyboard)
				
			elif r.text == "\"Do you want more books from this genre?\"":	
				genre = text
				res = get_next_message_by_genre(genre, chat)
				send_photo(res, chat);
				time.sleep(2)
				keyboard = '{"inline_keyboard" : [[{"text":"Thank you and Goodbye!","callback_data":"goodbye"}],[{"text":"Yesss! Go on!","callback_data":"Yes"}]]}'
				send_message(r.text,chat,keyboard)
				
			elif r.text == "\"Showing more books from this author\"":
				if text=="Yes":
					send_message(r.text,chat)
					send_photo(res,chat,begin=3,end=8);
					time.sleep(2)

			elif r.text == "\"Showing more books from this genre\"":
				if text=="Yes":
					send_message(r.text,chat)
					send_photo(res,chat,begin=3,end=8);
					time.sleep(2)

			elif r.text == "\"Showing more books from this title\"":
				if text=="Yes":
					send_message(r.text,chat)
					send_photo(res,chat,begin=3,end=8);
					time.sleep(2)
			elif r.text == "\"100\"":
				book = text;
				url =  HOST + "getAverageRating/{}/".format(book)
				_json = get_json(url)
				if _json['rating'] == "None":
					send_message("Sorry, I don't have any rating of this book", chat)
				else:
					send_message(_json['rating'], chat)
			elif r.text == "\"200\"":
				book = text;
				url =  HOST + "getComments/{}/".format(book)
				_json = get_json(url)
				if _json["comments"] == "None":
					send_message( "Sorry, I couldn't find any comment about this book", chat)
				else:
					length = 3 if  len(_json["comments"]) > 3 else len(_json["comments"])
					for i in range(0,length):
						send_message( "\"" + _json["comments"][i]["comment"] + "\"", chat)
			elif r.text == '\"Goodbye bookworm!\"':
				send_message(r.text, chat);
				counter = 0
				end_switch = True
			elif r.text == '\"What is your comment on this book?\"':
				book = text
				send_message(r.text, chat);
			elif r.text == '\"What is your rating from 1 to 5?\"':
				book = text
				keyboard = '{"inline_keyboard": [[{"text":"1", "callback_data":"1"},{"text":"2", "callback_data":"2"},{"text":"3", "callback_data":"3"},{"text":"4", "callback_data":"4"},{"text":"5", "callback_data":"5"}]]}'
				send_message(r.text, chat,keyboard);		
			elif r.text == '\"Your comment is saved!\"':
				comment = text
				url =  HOST + "addComment/{}/{}/{}/".format(book, user_id, comment)
				print(url)
				send_message(r.text, chat);
				r = requests.post(url)
			elif r.text == '\"Your rating is saved!\"':
				rating = text
				url =  HOST + "addRating/{}/{}/{}/".format(book, user_id, rating)
				print(url)
				send_message(r.text, chat);
				r = requests.post(url)
			else:
				send_message(r.text, chat);
				counter = counter+1
			last_chat = (text, chat);			
			last_update = update_id; 

		time.sleep(0.5);


if __name__ == '__main__':
	main();
