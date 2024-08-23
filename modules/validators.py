import re
from rest_framework.serializers import ValidationError
from rest_framework import serializers


class LinkValidator:
    def __init__(self, field):
        self.field = field
        self.regex = r'^(http|https)://[^\s/$.?#].[^\s]*$'  # Регулярное выражение для ссылок
        self.reg = re.compile(self.regex)

    def __call__(self, value):
        if value is not None:  # Проверка, чтобы валидировать только если значение не None
            if not isinstance(value, str):
                raise serializers.ValidationError("Значение должно быть строкой.")
            if not bool(self.reg.match(value)):
                raise serializers.ValidationError("Недопустимое значение.")


class CustomValidator:
    def init(self, regex):
        self.regex = regex
        self.reg = re.compile(self.regex)

    def call(self, value):
        if value is not None:  # Проверка, чтобы валидировать только если значение не None
            if not isinstance(value, str):
                raise serializers.ValidationError("Значение должно быть строкой.")
            if not bool(self.reg.match(value)):
                raise serializers.ValidationError("Недопустимое значение.")