from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiTypes
from rest_framework import serializers
from rest_framework.views import APIView
from .vertex import global_openapi_parameters
<<<<<<< HEAD
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import requests
=======
>>>>>>> 7c39f95bdcfce8350dacbc59cd0b02aad4221b55
import cohere
import os
import base64

co = cohere.Client(os.environ.get('COHERE_API_KEY'))


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)

"""parameters=[
    OpenApiParameter(name='Message', description='A Message to Send', required=True, type=str),
]"""

@extend_schema(
        tags=['Genie v1'], 
        parameters=global_openapi_parameters,
        request=ChatRequestSerializer,
        responses={200: ChatRequestSerializer},
        tags=['Genie v1'], 
        parameters=global_openapi_parameters,
        examples=[
            OpenApiExample(
                'Message Only Request',
                value={'message': 'What sort of tasks can you help with?'}
            )
        ]
    ) 
@api_view(['post'])
def make_cohere_chat_beta_request(request):
    serializer = ChatRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = serializer.validated_data['message']
    response = co.chat(
        message=message,
    )
    if response:
        return Response(response.text, status=status.HTTP_200_OK)
    else:
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)
    

# Stablity AI - https://platform.stability.ai/
engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv("STABILITY_API_KEY")

class ImageRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=1000)

@extend_schema(
        tags=['Genie v1'], 
        parameters=global_openapi_parameters,
        request=ImageRequestSerializer,
        responses={200: ImageRequestSerializer},
        examples=[
            OpenApiExample(
                'Text to Image Prompt',
                value={'prompt': 'A colorful abstract happy image with a mouse at the center.'}
            )
        ]
    ) 
@api_view(['post'])
def make_stability_image_request(request):
    serializer = ImageRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    prompt = serializer.validated_data['prompt']
    response = requests.post(
        f"{api_host}/v1/engines/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )

    data = response.json()
    print(data)

    for i, image in enumerate(data["artifacts"]):
        with open(f"./out/v1_txt2img_{i}.png", "wb") as f:
            f.write(base64.b64decode(image['base64']))