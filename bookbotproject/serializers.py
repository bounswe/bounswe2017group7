from rest_framework import serializers
from conversationtree.models import Node


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model= Node
        fields =('name','intent','parent','message')