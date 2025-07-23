from rest_framework import serializers
import re


def validate_youtube_link(value):
    pattern = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/"
    if value and not re.search(pattern, value):
        raise serializers.ValidationError("Разрешены только ссылки на YouTube.")
    return value
