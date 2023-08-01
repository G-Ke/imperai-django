from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import viewsets, permissions
from core.models import Profile, CustomUser
from drf_spectacular.utils import extend_schema
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

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema(tags=['Vertex Chat'])
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

@extend_schema(tags=['Vertex Chat'])
class VertexChatConfigViewSet(viewsets.ModelViewSet):
    queryset = VertexChatConfig.objects.all()
    serializer_class = VertexChatConfigSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

@extend_schema(tags=['Vertex Chat'])
class VertexChatExampleIOPairViewSet(viewsets.ModelViewSet):
    queryset = VertexChatExampleIOPair.objects.all()
    serializer_class = VertexChatExampleIOPairSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

@extend_schema(tags=['Vertex Chat Context'])
class VertexChatContextViewSet(viewsets.ModelViewSet):
    queryset = VertexChatContext.objects.all()
    serializer_class = VertexChatContextSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

@extend_schema(tags=['Vertex Chat Context'])
class VertexChatContextInstructViewSet(viewsets.ModelViewSet):
    queryset = VertexChatContextInstruct.objects.all()
    serializer_class = VertexChatContextInstructSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

@extend_schema(tags=['Vertex Chat Context'])
class VertexChatContextRuleViewSet(viewsets.ModelViewSet):
    queryset = VertexChatContextRule.objects.all()
    serializer_class = VertexChatContextRuleSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]

@extend_schema(tags=['Vertex Chat Context'])
class VertexChatContextDetailViewSet(viewsets.ModelViewSet):
    queryset = VertexChatContextDetail.objects.all()
    serializer_class = VertexChatContextDetailSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]