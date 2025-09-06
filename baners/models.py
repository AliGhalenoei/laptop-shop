from django.db import models
# Create your models here.


class BaseBanerModel(models.Model):
    baner = models.ImageField(upload_to="baners/header/")
    alt = models.CharField(max_length=100 , null=True,blank=True)
    link = models.URLField(max_length=255 , null=True , blank=True)
    
    class Meta:
        abstract = True
        

class BanerHeader(BaseBanerModel):
    class Meta:
        verbose_name = "بنر هدر سایت"
        verbose_name_plural = "بنرهای هدر سایت"

class BanerHomePage(BaseBanerModel):
    baner = models.ImageField(upload_to="baners/home_page/")

    class Meta:
        verbose_name = "بنر های صفحه خانه"
        verbose_name_plural = "بنر های صفحه خانه"
