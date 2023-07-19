from django.contrib import admin
from .models import VertexChatConfig, VertexChatExampleIOPair, VertexChatContext, VertexChatContextInstruct, VertexChatContextRule, VertexChatContextDetail, VertexChatRequest

# Register your models here.

admin.site.register(VertexChatConfig)
admin.site.register(VertexChatExampleIOPair)
admin.site.register(VertexChatContext)
admin.site.register(VertexChatContextInstruct)
admin.site.register(VertexChatContextRule)
admin.site.register(VertexChatContextDetail)
admin.site.register(VertexChatRequest)