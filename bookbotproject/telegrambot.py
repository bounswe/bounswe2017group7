import json
import requests
import time

TOKEN = "433004356:AAFzeqBEW8_UgEPDOnJ8bnQAPitaR7gLSSo";
URL = 	"https://api.telegram.org/bot{}/".format(TOKEN);

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

def get_last_chat(updates):
	length = len(updates["result"]);
	text = updates["result"][length-1]["message"]["text"];
	chat_id = updates["result"][length-1]["message"]["chat"]["id"];
	update_id = updates["result"][length-1]["update_id"]; 
	return [text, chat_id, update_id];

def get_next_message_by_response(text):
	# TODO This should calculate and return next message after wit.ai is ready
	return "jamiryo";

def send_message(message, chat_id):
	response = get_next_message_by_response(message);
	sendURL = URL + "sendMessage?text={}&chat_id={}".format(response, chat_id);
	send_request(sendURL);

def main():
	last_chat = (None, None);
	last_update = None;
	while True:
		text, chat, update_id = get_last_chat(get_updates(last_update));
		if(text, chat) != last_chat:
			send_message(text, chat);
			last_chat = (text, chat);			
			last_update = update_id; 
		time.sleep(0.5);


if __name__ == '__main__':
	main();
