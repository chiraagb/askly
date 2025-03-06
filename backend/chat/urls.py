from django.urls import path, include
from .views import (
    TextToPdf,
    SessionView,
    SessionChatsView,
    Summary,
    UploadPDFView,
    PDFUploadStatus,
    FetchSession,
)

urlpatterns = [
    path("text-to-pdf/", TextToPdf.as_view(), name="text-to-pdf"),
    path("session/", SessionView.as_view(), name="chat-session"),
    path("session/<int:pk>/", SessionView.as_view(), name="chat-session"),
    path(
        "session-chats/<int:session_id>/",
        SessionChatsView.as_view(),
        name="session-chats",
    ),
    path("session/fetch/<int:pdf_key>/", FetchSession.as_view(), name="fetch-session"),
    path(
        "session-summary/<int:session_id>/", Summary.as_view(), name="session-summary"
    ),
    path("pdf-upload/", UploadPDFView.as_view(), name="create-vector-store"),
    path(
        "pdf-upload-status/<int:pdf_key>/",
        PDFUploadStatus.as_view(),
        name="pdf-upload-status",
    ),
]
