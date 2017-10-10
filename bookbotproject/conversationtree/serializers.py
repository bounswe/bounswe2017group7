from rest_framework import serializers
from conversationtree.models import ConversationTree

class ConversationTreeSerializer(serializers.ModelSerializer):
 	class Meta:
        	model = ConversationTree
        	fields = ('id', 'title')
