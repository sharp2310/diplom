from rest_framework import serializers

from modules.models import Module


class ModuleSerializer(serializers.ModelSerializer):
    """Educational module serializer"""

    class Meta:
        model = Module
        fields = "__all__"