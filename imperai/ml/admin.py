from django.contrib import admin
from .models import VertexChatConfig, VertexChatExampleIOPair, VertexChatContext, VertexChatContextInstruct, VertexChatContextRule, VertexChatContextDetail, VertexChatRequest

# Register your models here.

admin.site.register(VertexChatConfig)

class VertexChatExampleIOPairAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    readonly_fields = ['created_at']
admin.site.register(VertexChatExampleIOPair, VertexChatExampleIOPairAdmin)

admin.site.register(VertexChatContext)
admin.site.register(VertexChatContextInstruct)
admin.site.register(VertexChatContextRule)
admin.site.register(VertexChatContextDetail)
admin.site.register(VertexChatRequest)