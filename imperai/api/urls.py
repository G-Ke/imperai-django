from django.urls import path, include
from rest_framework import routers
from . import vertex
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = routers.DefaultRouter()
router.register(r'user-management/users', vertex.UserViewSet)
router.register(r'user-management/groups', vertex.GroupViewSet)
router.register(r'vertex/chat/requests', vertex.VertexChatRequestViewSet)
router.register(r'vertex/chat/configs', vertex.VertexChatConfigViewSet)
router.register(r'vertex/chat/exampleiopairs', vertex.VertexChatExampleIOPairViewSet)
router.register(r'vertex/chat/contexts', vertex.VertexChatContextViewSet)
router.register(r'vertex/chat/contextinstructs', vertex.VertexChatContextInstructViewSet)
router.register(r'vertex/chat/contextrules', vertex.VertexChatContextRuleViewSet)
router.register(r'vertex/chat/contextdetails', vertex.VertexChatContextDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]