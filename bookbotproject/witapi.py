from wit import Wit
import json
import requests

access_token = "4UYTKEFBNBC7PKBSEHZL5KJ3MSKYALZ4"
client = Wit(access_token = access_token)

#returns the intent for a given input text
def get_Intent(input_text):
	response = client.message(input_text)
	intent = None
	value  = None
	#print(input_text)
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



# communication function between the other parts of the program and wit
# call this function with database templates to send it to wit
# this function calls other necessary functions
def send_data_to_wit(templates):
	tuples = prepare_tuples_from_templates(templates)	
	json_data = prepare_json_to_train(tuples)
	send_request_to_wit(json_data)


# this method sends the training data to wit api for it to train the system.
# data: must be given in proper json format
# the returned value from "prepare_json_to_train" method will be fed into this as parameter
def send_request_to_wit(data):
	url     = 'https://api.wit.ai/samples?v=20170307'
	headers = {"Authorization": "Bearer 4UYTKEFBNBC7PKBSEHZL5KJ3MSKYALZ4","Content-Type": "application/json" }
	res = requests.post(url, data=data, headers=headers)


# find the beginning position of a given substring in the given string. we use this for keyword extraction purposes
def find_str(s, subs):
    index = 0
    if subs in s:
        c = subs[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(subs)] == subs:
                    return index
            index += 1
    return -1


# extracts the keyword in a given sentence
def extract_keyword(sentence):
	words = sentence.split('*')
	return words[1].lower().title()

# prepares the json data which is to be sent to wit. 
# takes lists of three tuples as argument where a tuple = (template_Sentence, intent, keyword)
def prepare_json_to_train(template_Tuples):
	training_data = []
	for (template, intent, keyword) in template_Tuples:
		start_of_keyword = find_str(template,keyword)
		training_data.append({'text': template, 
							   'entities': 
								[
									{
									'entity':intent,
									'start':start_of_keyword, 
									'end' :start_of_keyword + len(keyword),
									'value':keyword
									}
								]
							 }
							)
	x = json.dumps(training_data)
	return x

# prepares the three tuples to be used for preparation of json_datax
def prepare_tuples_from_templates(templates):
	template_Tuples = []
	for i in range(len(templates)):
		template_Sentence = templates[i].template
		template_Tuples.append((template_Sentence.replace('*',''),templates[i].node.intent,extract_keyword(template_Sentence)))

	return template_Tuples