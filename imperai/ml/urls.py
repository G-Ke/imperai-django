from django.contrib import admin
from django.urls import path, include
from .views import (
    VertexChatWelcomeView, 
    VertexChatConfigStartView, 
    VertexChatConfigStartDetailCreateView, 
    VertexChatConfigStartInstructCreateView,
    VertexChatConfigStartRuleCreateView,
    VertexChatConfigStartReviewContextView,
    VertexChatConfigStartExampleCreateView,
    VertexChatConfigStartConnectView
    #create_examples
)

urlpatterns = [
    path('vertex', VertexChatWelcomeView.as_view(), name='vertex_chat_welcome'),
    path('vertex/configurator', VertexChatConfigStartView.as_view(), name='vertex_chat_config_start'),
    path('vertex/configurator/detail/create', VertexChatConfigStartDetailCreateView.as_view(), name='vertex_chat_config_start_detail_create'),
    path('vertex/configurator/instruct/create', VertexChatConfigStartInstructCreateView.as_view(), name='vertex_chat_config_start_instruct_create'),
    path('vertex/configurator/rule/create', VertexChatConfigStartRuleCreateView.as_view(), name='vertex_chat_config_start_rule_create'),
    path('vertex/configurator/review-context', VertexChatConfigStartReviewContextView.as_view(), name='vertex_chat_config_start_review_context'),
    path('vertex/configurator/example/create', VertexChatConfigStartExampleCreateView.as_view(), name='vertex_chat_config_start_example_create'),
    # path('vertex/configurator/example/create', create_examples, name='vertex_chat_config_start_example_create')
    path('vertex/configurator/connect', VertexChatConfigStartConnectView.as_view(), name='vertex_chat_config_start_connect'),
]