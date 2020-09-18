from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        # enforcing that there can not be two categories under a parent with same slug
        # __str__ method elaborated later in post.  use __unicode__ in place of
        # __str__ if you are using python 2
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])
    
    def __str__(self):
        return self.name

class Course(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    img = models.ImageField(upload_to='thumbnails')
    slug = models.SlugField(max_length=300, null=True, blank=True)
    body_text = RichTextUploadingField(null=True)
    course_hour = models.CharField(max_length=100)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    course_site_name = models.CharField(max_length=100, default='Site Name')
    url = models.URLField(null=True, blank=2)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.title

    def get_cat_list(self):
        k = self.category  # for now ignore this instance method

        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb) - 1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i - 1:-1])
        return breadcrumb[-1:0:-1]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=254)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    
    
    def __str__(self):
        return 'Message from' + self.name