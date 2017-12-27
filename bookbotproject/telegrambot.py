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
	name = updates["result"][length-1]["message"]["from"]["first_name"]
	user_id = updates["result"][length-1]["message"]["from"]["id"];
	text = updates["result"][length-1]["message"]["text"];
	chat_id = updates["result"][length-1]["message"]["chat"]["id"];
	update_id = updates["result"][length-1]["update_id"]; 
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
	
	book = goodReadsApi.search_by_title(text)
	
	return book

def send_message(message, chat_id):
	#response = get_next_message_by_response(message, chat_id);
	if(isinstance(message,list)):
		for index in message:
			sendURL = URL + "sendMessage?text={}&chat_id={}".format(index, chat_id);
			sendURL = sendURL.replace("#","No:")
			send_request(sendURL);
			time.sleep(0.3);
	else:
		print(chat_id)
		sendURL = URL + "sendMessage?text={}&chat_id={}".format(message, chat_id);
		sendURL = sendURL.replace("#","No:")
		
		send_request(sendURL);

def send_photo(works, chat_id):
	"""Sends five best books pictures alongside with information """
	newline = "%0A"
	count = 0
	for work in works:
		count +=1
		if(count>10):
			break
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
		print("before text = "+text)
		text = re.sub('[^A-Za-z0-9]+', ' ', text)
		print("after text = "+text)
		

		current_Node_r = requests.get(HOST + "getCurrentNode/{}/".format(user_id))		
		json_response = json.loads(current_Node_r.content)

		current_node_intent = json_response['intent']
		#print current_node_intent
		if(text, chat) != last_chat:
			# Get related response for user message
			r = requests.get(HOST + "getResponse/{}/{}/".format(text, chat))

			print(r.text)

			if end_switch and r.text == '\"Goodbye bookworm!\"':
				end_switch = True
			elif r.text == "\"Which genre's books are you looking for?\"" :
				end_switch = False
				temptext = text
				send_message(r.text,chat)
				while (temptext==text):
					text, chat, update_id, user_id = get_last_chat(get_updates(last_update))
					time.sleep(0.5)
				res = get_next_message_by_genre(text, chat)
				send_photo(res, chat);
				counter = 0
			elif r.text == "\"Which author's books are you looking for?\"" :
				end_switch = False
				temptext = text
				send_message(r.text,chat)
				while (temptext==text):
					text, chat, update_id, user_id = get_last_chat(get_updates(last_update))
					time.sleep(0.5)
				res = get_next_message_by_author(text, chat)
				send_photo(res, chat);
				counter = 0
			elif r.text == "\"Which subject are you looking for?\"" :
				end_switch = False
				temptext = text
				send_message(r.text,chat)
				while (temptext==text):
					text, chat, update_id, user_id = get_last_chat(get_updates(last_update))
					time.sleep(0.5)
				res = get_next_message_by_title(text, chat)
				send_photo(res, chat);
				counter = 0
			elif r.text == '\"Goodbye bookworm!\"':
				send_message(r.text, chat);
				counter = 0
				end_switch = True
			elif r.text == '\"What is your comment on this book?\"':
				book = text
				send_message(r.text, chat);
			elif r.text == '\"What is your rating from 1 to 5?\"':
				book = text
				send_message(r.text, chat);	
			elif r.text == '\"Your comment is saved!\"':
				comment = text
				url =  HOST + "addComment/{}/{}/{}/".format(book, user_id, comment)
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
