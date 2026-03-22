from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from core.views import UserViewSet, UserAiQuestionViewSet, FeedViewSet, ViewViewSet, LikeViewSet, SaveViewSet
from uploader.views import ImageUploadViewSet


router = DefaultRouter()

router.register("image", ImageUploadViewSet, basename="image")
router.register(r"question", UserAiQuestionViewSet, basename="question")
router.register(r'users', UserViewSet, basename='users')
router.register(r'feed', FeedViewSet, basename='feed')
router.register(r'views', ViewViewSet, basename='views')
router.register(r'likes', LikeViewSet, basename='likes')
router.register(r'saves', SaveViewSet, basename='saves')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui',),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc',),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)