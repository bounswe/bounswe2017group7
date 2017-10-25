from rest_framework import serializers
from conversationtree.models import Node
from conversationtree.models import TelegramUser


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model= Node
        fields =('name','intent','parent','message')

class TelegramUserSerializer(serializers.ModelSerializer):

    class Meta:
        model= TelegramUser
        fields =('name','userid','chatid','currentnode')