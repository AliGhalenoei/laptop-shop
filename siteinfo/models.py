from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.safestring import mark_safe

# Create your models here.


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = CKEditor5Field('Text', config_name='extends')

    class Meta:
        verbose_name = "سوالات متداول"
        verbose_name_plural = "سوالات متداول"

    def __str__(self):
        return self.question
    
class AboutUs(models.Model):
    content = CKEditor5Field('Text', config_name='extends')

    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"

class ContactUs(models.Model):
    content = CKEditor5Field('Text', config_name='extends')

    class Meta:
        verbose_name = "تماس با ما"
        verbose_name_plural = "ماس با ما"

