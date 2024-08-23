from django.urls import path

from modules.views import ModuleCreateAPIView, ModuleListAPIView, ModuleDetailAPIView, ModuleDestroyAPIView, \
    ModuleUpdateAPIView, SubscriptionView, SubscriptionListAPIView, LessonCreateAPIView, \
    LessonListAPIView, LessonDetailAPIView, LessonDestroyAPIView, LessonUpdateAPIView

app_name = 'modules'

urlpatterns = [
    # Модули
    path('create/', ModuleCreateAPIView.as_view(), name='module_create'),
    path('list/', ModuleListAPIView.as_view(), name='module_list'),
    path('detail/<int:pk>/', ModuleDetailAPIView.as_view(), name='module_detail'),
    path('delete/<int:pk>/', ModuleDestroyAPIView.as_view(), name='module_delete'),
    path('update/<int:pk>/', ModuleUpdateAPIView.as_view(), name='module_update'),
    # Уроки
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/list/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lessons/detail/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson_detail'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    # Подписка
    path('subscription/<int:pk>/', SubscriptionView.as_view(), name='module_subscription'),
    path('subscription/list/', SubscriptionListAPIView.as_view(), name='module_subscription_list'),
]