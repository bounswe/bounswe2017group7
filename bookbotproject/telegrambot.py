import json
import requests

TOKEN = "433004356:AAFzeqBEW8_UgEPDOnJ8bnQAPitaR7gLSSo";
URL = 	"https://api.telegram.org/not{}/".format(TOKEN);

def get_url(url):
	res = requests.get(url);
	content = res.content.decode("utf8");
	return content;


def get_json(url):
	content = get_url(url);
	retrieved_json = json.loads(content);
	return retrieved_json;


def get_updates():
	updateURL = URL + "getUpdates"
	_json = get_json(updateURL);
	return _json;

def get_last_chat(updates):
	length = len(updates["result"]);
	text = updates["resutl"][length-1]["message"]["text"];
	chat_id = updates["result"][length-1]["message"]["id"];
	return [text, chat_id];


