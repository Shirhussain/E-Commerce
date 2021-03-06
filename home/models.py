from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField



class Language(models.Model):
    name= models.CharField(max_length=20)
    code= models.CharField(max_length=5)
    status=models.BooleanField()
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

llist = Language.objects.filter(status=True)
list1 = []
for rs in llist:
    list1.append((rs.code,rs.name))
langlist = (list1)

class Settings(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )
    title = models.CharField(max_length=150)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=60)
    smtpserver = models.CharField(blank=True, max_length=50)
    smtpemail = models.CharField(blank=True, max_length=50)
    smtppassword = models.CharField(blank=True, max_length=20)
    smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to="settings_images")
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SettingLang(models.Model):
    setting = models.ForeignKey(Settings, on_delete=models.CASCADE)
    lang = models.CharField(max_length=8, choices=langlist)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )

    name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=60)
    subject = models.CharField(blank=True, max_length=55)
    message = models.CharField(blank=True, max_length=255)
    status = models.CharField(max_length=6, choices = STATUS, default="New")
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 


class FAQ(models.Model):
    STATUS = (
        ('True','True'),
        ('False','False'),
    )
    lang = models.CharField(max_length=8, choices = langlist, blank=True, null=True)
    ordernumber = models.IntegerField()
    question    = models.CharField(max_length=200)
    answer      = RichTextUploadingField()
    status      = models.CharField(max_length=5, choices=STATUS)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question