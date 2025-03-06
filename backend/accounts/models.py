from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField
import os


def document_upload_path(instance, filename):
    # You can use attributes of 'instance' (like 'instance.user.id' if your model has a 'user' attribute)
    # to create a file path. Here's a simple example:
    extension = os.path.splitext(filename)[1]
    new_filename = "custom_name" + extension  # Or any logic to set a new filename
    return os.path.join(
        f"documents/{instance.user.username}-{instance.user.id}/", new_filename
    )


def organization_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/organization_<id>/<filename>
    return "organization_{0}/{1}".format(instance.organization.id, filename)


class Organization(models.Model):
    name = models.CharField(max_length=100)


class OrganizationFile(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="files"
    )
    file = models.FileField(upload_to=organization_directory_path)


class User(AbstractUser):
    email = models.EmailField(_("Email address"), unique=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    assistant_id = models.CharField(max_length=100, null=True, blank=True)
    thread_id = models.CharField(max_length=100, null=True, blank=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="users"
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        creating = self._state.adding
        if creating:
            if not hasattr(self, "organization") or self.organization is None:
                # Automatically create and assign an organization
                organization = Organization.objects.create(
                    name=f"Organization for {self.username}"
                )
                self.organization = organization
        super().save(*args, **kwargs)


class Documents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    document = models.FileField(upload_to=document_upload_path)


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username


class Notification(models.Model):
    NOTIFICATION_CHOICES = [
        ("Email", "Email"),
        ("Mobile", "Mobile"),
    ]

    mobile = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_CHOICES)
    otp = models.IntegerField()
    count = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email if self.email else self.mobile
