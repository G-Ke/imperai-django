from django.contrib.auth.models import User, GroupManager, Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from ml.models import (
    VertexChatRequest, 
    VertexChatConfig, 
    VertexChatExampleIOPair,
    VertexChatContext,
    VertexChatContextInstruct,
    VertexChatContextRule,
    VertexChatContextDetail,
)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['url', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class VertexChatRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VertexChatRequest
        fields = ['url', 'id', 'user', 'chat_config', 'context', 'example', 'managed_status']


class VertexChatConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VertexChatConfig
        fields = '__all__'


class VertexChatExampleIOPairSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VertexChatExampleIOPair
        fields = '__all__'


class VertexChatContextSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VertexChatContext
        fields = '__all__'


class VertexChatContextInstructSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VertexChatContextInstruct
        fields = '__all__'


class VertexChatContextRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VertexChatContextRule
        fields = '__all__'

class VertexChatContextDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VertexChatContextDetail
        fields = '__all__'