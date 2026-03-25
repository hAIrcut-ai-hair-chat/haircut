from email.mime import image
import uuid
from cloudinary.models import CloudinaryField
from django.db import models


def image_file_path(instance, filename) -> str:
    """Legacy upload path helper for existing migrations."""
    return f"media/images/{filename}"


class Image(models.Model):
    attachment_key = models.UUIDField(
        max_length=255,
        default=uuid.uuid4,
        unique=True,
        help_text=("Used to attach the image to another object. " "Cannot be used to retrieve the image file."),
    )
    public_id = models.UUIDField(
        max_length=255,
        default=uuid.uuid4,
        unique=True,
        help_text=(
            "Used to retrieve the image itself. "
            "Should not be readable until the image is attached to another object."
        ),
    )
    file = CloudinaryField('image', folder="images/")
    description = models.CharField(max_length=255, blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.description} - {self.attachment_key}"

    @property
    def url(self) -> str:
        return self.file.url  # pylint: disable=no-member
