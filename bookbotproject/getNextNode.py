from witapi import get_Intent
from conversationtree.models import *
from telegrambot import *


def getNextNode(input_text, telegram_user):
	intent_ret = get_Intent(input_text)

	curr_node = telegram_user.currentnode


	for i in range(len(curr_node.get_children())):
		if intent_ret == curr_node.get_children()[i].intent:
			telegram_user.currentnode=curr_node.get_children()[i]
			send_message(telegram_user.currentnode.message,telegram_user.chatid)