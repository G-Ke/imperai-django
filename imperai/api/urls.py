from django.urls import path, include
from rest_framework import routers
from . import vertex, genie, together
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views
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
# router.register(r'genie/chat/beta', genie.CohereChatBetaRequestView, basename='cohere')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # path('genie/chat/beta', genie.CohereChatBetaRequestView.as_view(), name='cohere'),
    path('genie/chat/beta', genie.make_cohere_chat_beta_request, name='genie-chat-beta'),
    path('genie/image/', genie.make_stability_image_request, name='genie-image'),
    path('together/models', together.get_together_models, name='together-models'),
    path('together/chat', together.send_together_chat_completion, name='together-chat')
]