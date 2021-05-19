from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name="Is deleted")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        abstract = True


class BaseUserModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")

    class Meta:
        abstract = True
