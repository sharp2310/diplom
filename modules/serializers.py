from rest_framework import serializers
from modules.models import Module, Lesson, Subscription
from modules.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для урока"""

    video_link = serializers.CharField(required=False, validators=[LinkValidator(field="video_link")])

    class Meta:
        model = Lesson
        fields = (
            "pk",
            "module",
            "title",
            "description",
            "preview",
            "video_link",
            "owner",
        )
        read_only_fields = ['owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user  # Установка текущего пользователя как владельца
        return super().create(validated_data)



class ModuleSerializer(serializers.ModelSerializer):
    """Сериализатор для модуля"""
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:  # Проверка на аутентифицированного пользователя
            return Subscription.objects.filter(user=user, module=obj).exists()
        return False

    class Meta:
        model = Module
        fields = (
            "pk",
            "title",
            "description",
            "preview",
            "lessons",
            "lessons_count",
            "is_subscribed",
            "owner",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки"""
    module_name = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()

    def get_module_name(self, obj):
        return obj.module.title

    def get_user_email(self, obj):
        return obj.user.email

    class Meta:
        model = Subscription
        fields = "__all__"
        extra_fields = ["module_title", "user_email"]