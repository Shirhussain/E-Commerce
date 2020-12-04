from django.db import models
from django.utils.safestring import mark_safe
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


# here in category and sub category i will use mptt 
# MPTT is a technique for storing hierarchical data in a database.
class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='category_images/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title   
    
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
    

    class MPTTMeta:
        order_insertion_by = ['title']

    # to undrestand better the parrent and child i'm gonna separated by '/' from each other
    def __str__(self):
        full_path = [self.title]
        c = self.parent
        while c is not None:
            full_path.append(c.title)
            c = c.parent
        return ' / '.join(full_path[::-1])


    

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='product_images/')
    price = models.FloatField()
    amount=models.IntegerField()
    minamount=models.IntegerField()
    detail= RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


    # method to create a fake table field in read only mode
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to="images")

    def __str__(self):
        return self.title
