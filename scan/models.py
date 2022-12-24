
from datetime import date

from django.conf import settings
from django.db import models


def user_directory_path(instance, filename):
    return f'uploads/user_{instance.user.username}/{date.today():%Y/%m/%d}/{filename}'


# Create your models here.
class Uploads(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )

    image = models.ImageField(upload_to=user_directory_path)
    caption = models.CharField(max_length=8, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image.url} - {self.user.username}"

    def __repr__(self) -> str:
        return f"Uploads(user={self.user.username}, image={self.image.url})"
