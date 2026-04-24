from rest_framework import serializers


class SyncRequestSerializer(serializers.Serializer):
    creates = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    updates = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    deletes = serializers.ListField(child=serializers.DictField(), required=False, default=list)


class SyncResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    created_count = serializers.IntegerField()
    updated_count = serializers.IntegerField()
    deleted_count = serializers.IntegerField()
