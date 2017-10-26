from wit import Wit

access_token = "4UYTKEFBNBC7PKBSEHZL5KJ3MSKYALZ4"
client = Wit(access_token = access_token)


def get_Intent(input_text):
	response = client.message(input_text)

	intent = None
	value  = None
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


		
