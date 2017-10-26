import json
import requests
import time
import goodReadsApi

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

	return [text, chat_id, update_id];

def get_next_message_by_response(text, chat_id):
	### WARNING ###
	"""some processess we can make in this method, these methods and calls are not working."""
	"""in node structure, maybe we can make some definition to make a search on api"""
	
	"""intent = witapi.getIntent(text)
	user = findUserByChatId(chat_id)
	for node in user.currentnode.getChildren: 
		if (node.intent == intent):
			return node.message"""
	# TODO This should calculate and return next message after wit.ai is ready
	print(text)
	"""if intent is determined by the wit.ai we can search by author"""
	#book = goodReadsApi.search_by_genre(text)
	print(book[0])
	## BUG DETECTED
	#sometimes these searches returns multiple dimensional arrays. when it happens no message returns to the user. for exmple: make a search_by_author("dan brown")
	# we need to handle this bug
	return book[0]

def send_message(message, chat_id):
	#response = get_next_message_by_response(message, chat_id);
	sendURL = URL + "sendMessage?text={}&chat_id={}".format(message, chat_id);
	send_request(sendURL);


def main():
	last_chat = (None, None);
	last_update = None;
	while True:
		text, chat, update_id = get_last_chat(get_updates(last_update));
		if(text, chat) != last_chat:
			r = requests.get(HOST + "getResponse/{}/{}/".format(text, chat))
			send_message(r.text, chat);
			print("message sent")
			last_chat = (text, chat);			
			last_update = update_id; 

		time.sleep(0.5);


if __name__ == '__main__':
	main();


