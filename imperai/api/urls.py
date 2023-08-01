from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'vertex/chat/requests', views.VertexChatRequestViewSet)
router.register(r'vertex/chat/configs', views.VertexChatConfigViewSet)
router.register(r'vertex/chat/exampleiopairs', views.VertexChatExampleIOPairViewSet)
router.register(r'vertex/chat/contexts', views.VertexChatContextViewSet)
router.register(r'vertex/chat/contextinstructs', views.VertexChatContextInstructViewSet)
router.register(r'vertex/chat/contextrules', views.VertexChatContextRuleViewSet)
router.register(r'vertex/chat/contextdetails', views.VertexChatContextDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]