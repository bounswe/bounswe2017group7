from wit import Wit

access_token = "4UYTKEFBNBC7PKBSEHZL5KJ3MSKYALZ4"
client = Wit(access_token = access_token)


def get_Intent(input_text):
	response = client.message(input_text)
	intent = None
	value  = None
	print(input_text)
	try:
		#Find the intent suggested by Wit
		intent = response['entities'].keys()[0]
		#Find the value in the given text corresponding to that intent
		value  = response['entities'][intent][0]['value']

	except:
		pass

	return intent


#given a file containing train sentences line by line, we may train our app on Wit.ai
def auto_train_by_File(file_):
	f = open(file_)
	sentences = f.readlines()
	f.close()
	sentences = [sentence[:-1] if sentence.endswith("\n") else sentence for sentence in sentences]
	for sentence in sentences:
		client.message(sentence)


#This function creates JSON format of intent- template message from our database. 
#This function will be used to send training data to wit.api

def template_feed_get_json():
	dict_temps={}
	for i in range(len(templates)):
		dict_temps[templates[i].node.intent] = templates[i].template
	json_data = json.dumps(dict_temps)	
	return json_data

		
