from django.contrib import admin
from .models import (
    SessionChatHistory,
    Session,
    Assistant,
    AssistantFile,
    AssitantVectorStore,
)

# Register your models here.


admin.site.register(SessionChatHistory)

from .models import Session


class SessionAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "created_at", "updated_at")

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is when the obj is already created i.e. we're editing
            return ("created_at", "updated_at") + self.readonly_fields
        return self.readonly_fields


admin.site.register(Session, SessionAdmin)
admin.site.register(Assistant)
admin.site.register(AssistantFile)
admin.site.register(AssitantVectorStore)
