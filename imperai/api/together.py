import os
import together
import requests
import json
from rest_framework import viewsets, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, extend_schema_serializer, OpenApiExample, OpenApiParameter, OpenApiTypes, OpenApiResponse
from rest_framework import serializers
from .vertex import global_openapi_parameters
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page

key = os.environ.get('TOGETHER_API_KEY')
stop_seq = ["</s>", "[/INST]"]

class TogetherModelNameSerializer(serializers.Serializer):
    model_name = serializers.CharField(max_length=160)

class TogetherChatMessageSerializer(serializers.Serializer):
    role = serializers.CharField(default="user", max_length=10)
    content = serializers.CharField(default="What is the capital of France?", max_length=1000)

class TogetherChatRequestSerializer(serializers.Serializer):
    model = serializers.CharField(default="mistralai/Mixtral-8x7B-Instruct-v0.1")
    max_tokens = serializers.IntegerField(default=512)
    stop = serializers.ListField(child=serializers.CharField(default=stop_seq))
    temperature = serializers.FloatField(default=0.7)
    #messages = serializers.ListField(child=serializers.CharField())
    messages = serializers.ListField(child=TogetherChatMessageSerializer())
    top_p = serializers.FloatField(default=0.7)
    top_k = serializers.IntegerField(default=50)
    repetition_penalty = serializers.IntegerField(default=1)

class MessageSerializer(serializers.Serializer):
    role = serializers.CharField()
    content = serializers.CharField()

class ChoiceSerializer(serializers.Serializer):
    finish_reason = serializers.CharField()
    message = MessageSerializer()
    index = serializers.IntegerField()

class UsageSerializer(serializers.Serializer):
    prompt_tokens = serializers.IntegerField()
    completion_tokens = serializers.IntegerField()
    total_tokens = serializers.IntegerField()


@extend_schema_serializer(
    many=True,
    examples=[
        OpenApiExample(
            'Standard Success',
            summary='Successful chat',
            description='This is a longer description of a standard chat response.',
            value={
                "id": "84864c20d8c0306b-BOS",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": "Paris is the capital of France."
                        }
                    }
                ],
                "usage": {
                    "prompt_tokens": 13,
                    "completion_tokens": 6,
                    "total_tokens": 19
                },
                "created": 1636493475,
                "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "object": "chat.completion"
            },
            response_only=True,  # signal that example only applies to responses
        ),
        OpenApiExample(
            'Unauthorized Error',
            summary='Unauthorized chat',
            description='This is a longer description of an error chat response.',
            value={
                "detail": "Authentication credentials were not provided."
            },
            response_only=True,
            status_codes=['401'],
        ),
    ],
)
class TogetherChatResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    choices = serializers.ListField(child=ChoiceSerializer())
    usage = UsageSerializer()
    created = serializers.IntegerField()
    model = serializers.CharField()
    object = serializers.CharField()

    response_example = {
        "id": "84864c20d8c0306b-BOS",
        "choices": [
            {
            "finish_reason": "stop",
            "message": {
                "role": "assistant",
                "content": "The capital of Uganda is Kampala. Established in 1890, Kampala now serves as the country's industrial and commercial hub. It is located in the southern part of Uganda, near Lake Victoria. The city has a population of approximately 1.7 million people, making it the largest city and the principal administrative center in Uganda."
            },
            "index": 0
            }
        ],
        "usage": {
            "prompt_tokens": 18,
            "completion_tokens": 80,
            "total_tokens": 98
        },
        "created": 1705743013,
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "object": "chat.completion"
    }

@extend_schema(
    tags=['Together'], 
    parameters=global_openapi_parameters,
    request=None,
    responses={
        200: TogetherModelNameSerializer(many=True),
    }
)
@cache_page(60 * 15)
@api_view(['GET'])
def get_together_models(request):
    print(request.headers)
    model_list = together.Models.list()
    print(f'{len(model_list)} models available')
    model_names = [model_dict['name'] for model_dict in model_list]
    if model_names:
        # return Response(model_names[:150], status=status.HTTP_200_OK)
        recommended_models = [
            'togethercomputer/llama-2-70b-chat',
            'togethercomputer/llama-2-13b-chat',
            'togethercomputer/llama-2-7b-chat',
            'codellama/CodeLlama-70b-Instruct-hf',
            'codellama/CodeLlama-34b-Instruct-hf',
            'codellama/CodeLlama-13b-Instruct-hf',
            'codellama/CodeLlama-7b-Instruct-hf',
            'mistralai/Mistral-7B-Instruct-v0.2',
            'togethercomputer/Llama-2-7B-32K-Instruct',
            'Austism/chronos-hermes-13b'
        ]
        served_chat_models = []
        for rm in recommended_models:
            if rm in model_names:
                served_chat_models.append(rm)
        #served_chat_models = [{'model_name': model} for model in served_chat_models]
        #serializer = TogetherModelNameSerializer(served_chat_models, many=True)
        return Response(served_chat_models, status=status.HTTP_200_OK)
    else:
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Together'], 
    parameters=global_openapi_parameters,
    request=TogetherChatRequestSerializer,
    responses={
        200: TogetherChatResponseSerializer,
        401: TogetherChatResponseSerializer
    }
)
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def send_together_chat_completion(request):
    url = "https://api.together.xyz/v1/chat/completions"
    print(request.data)
    pl = {
        "model": request.data['model'],
        "max_tokens": request.data['max_tokens'],
        "stop": ["</s>", "[/INST]"],
        "temperature": request.data['temperature'],
        "top_p": request.data['top_p'],
        "top_k": request.data['top_k'],
        "repetition_penalty": request.data['repetition_penalty'],
        "messages": request.data['messages']
    }

    payload_example = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "max_tokens": 512,
        "stop": ["</s>", "[/INST]"],
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "messages": [
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ]
    }

    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'Authorization': f"Bearer {key}"
    }

    response_data = requests.post(url, json=pl, headers=headers)
    response = response_data.json()
    #print(response)
    return Response(response)