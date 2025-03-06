from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import SessionChatHistory, Session, AssistantFile
from rest_framework import serializers
from .models import SessionChatHistory, Session, AssistantFile


class SessionSerializer(ModelSerializer):
    file = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields = ["id", "name", "file"]

    def get_file(self, obj):
        assistant_file = AssistantFile.objects.filter(vectorstore=obj.vectorstore).first()
        if assistant_file and assistant_file.file:
            return assistant_file.file.url
        return None




class SessionChatsSerailzer(ModelSerializer):
    class Meta:
        model = SessionChatHistory
        fields = ["message", "is_user_message"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["client"] = ret.pop("is_user_message")
        return ret
