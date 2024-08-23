from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    get_object_or_404, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from modules.models import Module, Subscription, Lesson
from modules.paginators import ModulePagination
from modules.permissions import IsOwnerOrAdmin
from modules.serializers import ModuleSerializer, SubscriptionSerializer, LessonSerializer
from rest_framework.response import Response


class IndexView(TemplateView):
    """Контроллер просмотра домашней страницы"""
    template_name = 'modules/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = Module.objects.all()  # Получаем все модули
        return context

class ModuleCreateAPIView(CreateAPIView):
    """ Создание модуля """
    serializer_class = ModuleSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        # Устанавливаем владельца модуля как текущего пользователя
        serializer.save(owner=self.request.user)


class ModuleListAPIView(ListAPIView):
    """ Контроллер просмотра списка модулей """
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    pagination_class = ModulePagination


class ModuleDetailAPIView(RetrieveAPIView):
    """ Подробная информация о модуле """
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsAuthenticated]

class ModuleDestroyAPIView(DestroyAPIView):
    """ Удаление модуля """
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsOwnerOrAdmin]


class ModuleUpdateAPIView(UpdateAPIView):
    """ Редактирование модуля """
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def perform_update(self, serializer):
        """ Обновление модуля """
        serializer.save()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class LessonCreateAPIView(CreateAPIView):
    """Создание урока"""
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        # Устанавливаем владельца модуля как текущего пользователя
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """Список уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDetailAPIView(RetrieveAPIView):
    """Подробная информация об уроке"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Подсчет просмотров"""
        data = super().get_object()
        data.views_count += 1
        data.save()
        return data


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrAdmin]

class LessonUpdateAPIView(RetrieveUpdateAPIView):
    """Редактирование урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class SubscriptionView(APIView):
    """ Подписка на модуль """
    def post(self, request, pk, *args, **kwargs):
        user = request.user
        module = get_object_or_404(Module, pk=pk)

        if module:
            subscription, created = Subscription.objects.get_or_create(user=user, module=module)
            if created:
                message = 'Подписка оформлена'
            else:
                subscription.delete()
                message = 'Подписка отменена'
            return Response({'message': message}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Модуль не найден'}, status=status.HTTP_404_NOT_FOUND)

class SubscriptionListAPIView(ListAPIView):
    """ Список подписок для текущего пользователя """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]  # Убедитесь, что пользователь аутентифицирован

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(user=user)  # Возвращаем подписки только для текущего пользователя