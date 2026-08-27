from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(allow_blank=False, max_length=2000)
    session_id = serializers.UUIDField(required=False)


class SourceSerializer(serializers.Serializer):
    title = serializers.CharField()
    snippet = serializers.CharField()


class ChatResponseSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    reply = serializers.CharField()
    sources = SourceSerializer(many=True)
