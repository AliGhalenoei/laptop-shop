from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from accounts.models import User
# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE,related_name="comments")
    message = models.TextField(max_length=300)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.user.username