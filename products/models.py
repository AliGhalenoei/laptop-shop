from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment
from accounts.models import User
# Create your models here.



class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200 , unique=True)
    image = models.ImageField(upload_to="categorys/")
    sub_category = models.ForeignKey("self", on_delete=models.CASCADE , related_name="sub_categorys" , null=True , blank=True)
    is_sub = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.sub_category:
            self.is_sub = True
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ManyToManyField(Category , related_name="categorys")
    baner = models.ImageField(upload_to="baners/")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200 , unique=True)
    description = CKEditor5Field('Text', config_name='extends')
    price = models.DecimalField(max_digits=10 , decimal_places=0)  
    sale_price = models.DecimalField(max_digits=10 , decimal_places=0 , null=True , blank=True)   
    discount_off = models.PositiveIntegerField(default=0 , null=True , blank=True) 
    stock = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    comments = GenericRelation(Comment)
    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.sale_price and self.price > 0:
            discount_value = self.price - self.sale_price
            self.discount_off = round((discount_value / self.price) * 100)
        else:
            self.discount_off = 0
        
        super().save(*args, **kwargs)

class GaleryProduct(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="galerys")
    image = models.ImageField(upload_to="galerys/")

    class Meta:
        verbose_name = "گالری محصول"
        verbose_name_plural = "گالری محصولات"


class Bookmark(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="bookmarks")
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user {self.user.username} Saves Product {self.product.title}"
