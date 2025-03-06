import os

from accounts.models import Organization, OrganizationFile
from config.settings import DEFAULT_OPENAI_MODEL
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from openai import OpenAI

from .managers import AssistantManager, AssitantVectorstoreManager

# Create your models here.

User = get_user_model()
client = OpenAI()


def organization_directory_path(instance, filename):

    return "organization_{0}/{1}".format(instance.organization.id, filename)


def custom_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    user_related_name = f"{instance.user.pk} {instance.user.first_name}/"
    unique_filename = f"{filename}.{ext}"
    return os.path.join("pdfs/", user_related_name, unique_filename)


class PdfDetail(models.Model):
    STATUS_CHOICES = [
        ("Started", "Started"),
        ("Load Data", "Loading Data"),
        ("Create DB", "Creating DB"),
        ("Summarize", "Summarizing"),
        ("Completed", "Completed"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pdfs")
    name = models.CharField(max_length=500)
    key = models.CharField(max_length=500, unique=True, default="abc")
    pdf_file = models.FileField(
        upload_to="pdfs/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    uploaded_at = models.DateTimeField(default=timezone.now)
    sample_questions = models.TextField(default="")

    def clean(self):
        if not self.pdf_file.name.endswith(".pdf"):
            raise ValidationError(("Only PDF files are allowed."))


class Assistant(models.Model):
    assistant_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    instructions = models.TextField()
    model = models.CharField(max_length=100, default=DEFAULT_OPENAI_MODEL)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)

    def update_with_assistant(self, assistant_id, vectorstore, **kwargs):
        print(vectorstore)
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        self.assistant_id = assistant_id

        self.full_clean()
        self.save()

        vectorstore.assistant = self
        vectorstore.save()

        assistant_kwargs = {}

        name = kwargs.get("name")
        model = kwargs.get("model")
        instructions = kwargs.get("instructions")

        if name:
            assistant_kwargs["name"] = name
        if model:
            assistant_kwargs["model"] = model
        if instructions:
            assistant_kwargs["instructions"] = instructions

        client.beta.assistants.update(assistant_id=assistant_id, **assistant_kwargs)

    def delete_with_assistant(self):
        client.beta.assistants.delete(assistant_id=self.assistant_id)

    objects = AssistantManager()


class AssitantVectorStore(models.Model):
    name = models.CharField(max_length=100)
    vector_store_id = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    objects = AssitantVectorstoreManager()


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    name = models.CharField(max_length=100)
    vectorstore = models.ForeignKey(
        AssitantVectorStore,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sessions",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        if hasattr(self, "thread"):
            try:
                client.beta.threads.delete(thread_id=self.thread.thread_id)
            except Exception as e:
                print(e)
            self.thread.delete()
        return super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Thread(models.Model):
    thread_id = models.CharField(max_length=100)
    session = models.OneToOneField(
        Session, on_delete=models.CASCADE, related_name="thread"
    )


class SessionChatHistory(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="chat_history"
    )
    message = models.TextField()
    is_user_message = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)


class AssistantFile(models.Model):
    name = models.CharField(max_length=100)
    vectorstore = models.ForeignKey(
        AssitantVectorStore, on_delete=models.SET_NULL, null=True, blank=True
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    file = models.FileField(upload_to=organization_directory_path)
    # file_id = models.CharField(max_length=100)
