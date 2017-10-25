from wit import Wit

access_token = "4UYTKEFBNBC7PKBSEHZL5KJ3MSKYALZ4"
client = Wit(access_token = access_token)


def get_Intent(input_text):
	response = client.message(input_text)

	#Find the intent suggested by Wit
	intent = response['entities'].keys()[0]

	#Find the value in the given text corresponding to that intent
	value  = response['entities'][intent][0]['value']

	return intent,value