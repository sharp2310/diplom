from rest_framework.routers import DefaultRouter

from edu_modules.apps import EduModulesConfig
from edu_modules.views import ModuleViewSet

app_name = EduModulesConfig.name

router = DefaultRouter()
router.register(r'module', ModuleViewSet, basename='module')

urlpatterns = [] + router.urls