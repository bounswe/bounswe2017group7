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
	print retrieved_json;
	return retrieved_json;


def get_updates():
	updateURL = URL + "getUpdates"
	_json = get_json(updateURL);
	print "updates!!!!!";
	print _json;
	return _json;

def get_last_chat(updates):
	length = len(updates["result"]);
	text = updates["result"][length-1]["message"]["text"];
	chat_id = updates["result"][length-1]["message"]["chat"]["id"];
	return [text, chat_id];

def send_message(chat_id):
	sendURL = URL + "sendMessage?text={}&chat_id={}".format("jamiryo",chat_id);
	send_request(sendURL);

def main():
	last_chat = (None, None);
	while True:
		text, chat = get_last_chat(get_updates());
		if(text, chat) != last_chat:
			send_message(chat);
			last_chat = (text, chat);
		time.sleep(0.5);


if __name__ == '__main__':
	main();
