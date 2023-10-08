from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import viewsets, permissions
from core.models import Profile, CustomUser
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiTypes 
from .serializers import (
    UserSerializer,
    GroupSerializer,
    VertexChatRequestSerializer,
    VertexChatConfigSerializer,
    VertexChatExampleIOPairSerializer,
    VertexChatContextSerializer,
    VertexChatContextInstructSerializer,
    VertexChatContextRuleSerializer,
    VertexChatContextDetailSerializer
)
from ml.models import (
    VertexChatRequest, 
    VertexChatConfig, 
    VertexChatExampleIOPair,
    VertexChatContext,
    VertexChatContextInstruct,
    VertexChatContextRule,
    VertexChatContextDetail,
)

global_openapi_parameters = [
    OpenApiParameter(
        name='Allow',
        type=str,
        location=OpenApiParameter.HEADER,
        response=True,
    ),
    OpenApiParameter(
        name='Content-Length',
        type=str,
        location=OpenApiParameter.HEADER,
        response=True,
    ),
    OpenApiParameter(
        name='Content-Type',
        type=str,
        location=OpenApiParameter.HEADER,
        response=True,
    ),
    OpenApiParameter(
        name='Cross-Origin-Opener-Policy',
        type=str,
        location=OpenApiParameter.HEADER,
        response=True,
    ),
    OpenApiParameter(
        name='Date',
        type=str,
        location=OpenApiParameter.HEADER,
        response=True,
    ),
    OpenApiParameter(
        name='Referrer-Policy',
        type=str,
        location=OpenApiParameter.HEADER,
        response=True,
    ),
    OpenApiParameter(
        name='Server',
        type=str,
        location=OpenApiParameter.HEADER,
        response=True,
    ),
    OpenApiParameter(
        name='Vary',
        type=str,
        location=OpenApiParameter.HEADER,
        response=True,
    ),

    OpenApiParameter(
        name='X-Frame-Options',
        type=str,
        location=OpenApiParameter.HEADER,
        response=True,
    ),
    OpenApiParameter(
        name='X-Content-Type-Options',
        type=str,
        location=OpenApiParameter.HEADER,
        response=True,
    ),
]


@extend_schema(tags=['User Management'], parameters=global_openapi_parameters)
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return CustomUser.objects.filter(id=user_id)


@extend_schema(tags=['User Management'], parameters=global_openapi_parameters)
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    tags=['Vertex Chat'],
    parameters=global_openapi_parameters,
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
            }
        )
    ]
)
class VertexChatRequestViewSet(viewsets.ModelViewSet):
    queryset = VertexChatRequest.objects.all()
    serializer_class = VertexChatRequestSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return VertexChatRequest.objects.all()
        else:
            return VertexChatRequest.objects.filter(user=self.request.user)

@extend_schema(tags=['Vertex Chat'], parameters=global_openapi_parameters)
class VertexChatConfigViewSet(viewsets.ModelViewSet):
    queryset = VertexChatConfig.objects.all()
    serializer_class = VertexChatConfigSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return VertexChatConfig.objects.filter(user=user)

@extend_schema(tags=['Vertex Chat'], parameters=global_openapi_parameters)
class VertexChatExampleIOPairViewSet(viewsets.ModelViewSet):
    queryset = VertexChatExampleIOPair.objects.all()
    serializer_class = VertexChatExampleIOPairSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return VertexChatExampleIOPair.objects.filter(user=user)

@extend_schema(tags=['Vertex Chat Context'], parameters=global_openapi_parameters)
class VertexChatContextViewSet(viewsets.ModelViewSet):
    queryset = VertexChatContext.objects.all()
    serializer_class = VertexChatContextSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return VertexChatContext.objects.filter(user=user)

@extend_schema(tags=['Vertex Chat Context'], parameters=global_openapi_parameters)
class VertexChatContextInstructViewSet(viewsets.ModelViewSet):
    queryset = VertexChatContextInstruct.objects.all()
    serializer_class = VertexChatContextInstructSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return VertexChatContextInstruct.objects.filter(user=user)


@extend_schema(tags=['Vertex Chat Context'], parameters=global_openapi_parameters)
class VertexChatContextRuleViewSet(viewsets.ModelViewSet):
    queryset = VertexChatContextRule.objects.all()
    serializer_class = VertexChatContextRuleSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return VertexChatContextRule.objects.filter(user=user)


@extend_schema(tags=['Vertex Chat Context'], parameters=global_openapi_parameters)
class VertexChatContextDetailViewSet(viewsets.ModelViewSet):
    queryset = VertexChatContextDetail.objects.all()
    serializer_class = VertexChatContextDetailSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return VertexChatContextDetail.objects.filter(user=user)
