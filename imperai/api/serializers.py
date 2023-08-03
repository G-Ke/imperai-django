from django.contrib.auth.models import User, GroupManager, Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
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

@extend_schema_serializer(
    examples = [
        OpenApiExample(
            'Example 1',
            summary='short summary',
            description='longer description',
            value={
                "count": 'integer',
                "next": 'string',
                "previous": 'string',
                "results": [
                    {
                        "url": "http://127.0.0.1:8000/api/v1/vertex/chat/requests/3b92de90-a4f3-4fa1-91bd-badfcdb138d2/",
                        "id": "3b92de90-a4f3-4fa1-91bd-badfcdb138d2",
                        "user": "http://127.0.0.1:8000/api/v1/users/2/",
                        "chat_config": "http://127.0.0.1:8000/api/v1/vertex/chat/configs/2201e2bf-3378-47a6-a147-947d164949c9/",
                        "context": "http://127.0.0.1:8000/api/v1/vertex/chat/contexts/f3f982ad-6104-47ed-8754-23f8633b3cb7/",
                        "example": [
                            "http://127.0.0.1:8000/api/v1/vertex/chat/exampleiopairs/ecebd885-5a3f-4908-9e01-c63dc13dc6b0/"
                        ],
                        "managed_status": 1
                    }
                ]
            },
        )
    ]
)
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