from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import os
from django.utils.html import mark_safe

class Note(models.Model):
    STATUS_CHOICES = [
        (True, "فعال"),
        (False, "بایگانی‌شده")
    ]
    
    title = models.CharField(max_length=250,unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique=True, blank=True, db_index=True)
    image = models.ImageField(upload_to='images', blank=True)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug or not self.pk:
            self.slug = slugify(self.title)  
        super().save(*args, **kwargs)  


      

    def delete(self, *args, **kwargs):
        if self.image:
            image_path = self.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)


    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" height="100" style="border-radius: 8px;" />')
        return "No Image"

    image_tag.short_description = 'Preview'

    class Meta:
        ordering = ["-created_at"] 
